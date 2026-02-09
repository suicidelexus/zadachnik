from flask import Blueprint, request, jsonify
from models import db, Task, Tag, RiceIdea

rice_bp = Blueprint('rice_api', __name__)


# === Priority Score Ideas API ===

@rice_bp.route('/api/rice-ideas', methods=['GET'])
def get_rice_ideas():
    """Получить все Priority Score-идеи, отсортированные по score"""
    ideas = RiceIdea.query.order_by(RiceIdea.rice_score.desc().nullslast()).all()
    return jsonify([idea.to_dict() for idea in ideas])


@rice_bp.route('/api/rice-ideas', methods=['POST'])
def create_rice_idea():
    """Создать новую Priority Score-идею"""
    data = request.json

    idea = RiceIdea(
        title=data.get('title'),
        description=data.get('description'),
        value=data.get('value'),
        reach=data.get('reach'),
        confidence=data.get('confidence'),
        budget_impact=data.get('budget_impact', 1.0)
    )

    # Вычисляем Priority Score
    idea.calculate_rice_score()

    db.session.add(idea)
    db.session.commit()

    return jsonify(idea.to_dict()), 201


@rice_bp.route('/api/rice-ideas/<int:idea_id>', methods=['GET'])
def get_rice_idea(idea_id):
    """Получить Priority Score-идею по ID"""
    idea = RiceIdea.query.get_or_404(idea_id)
    return jsonify(idea.to_dict())


@rice_bp.route('/api/rice-ideas/<int:idea_id>', methods=['PUT'])
def update_rice_idea(idea_id):
    """Обновить Priority Score-идею"""
    idea = RiceIdea.query.get_or_404(idea_id)
    data = request.json

    if 'title' in data:
        idea.title = data['title']
    if 'description' in data:
        idea.description = data['description']
    if 'value' in data:
        idea.value = data['value']
    if 'reach' in data:
        idea.reach = data['reach']
    if 'confidence' in data:
        idea.confidence = data['confidence']
    if 'budget_impact' in data:
        idea.budget_impact = data['budget_impact']

    # Пересчитываем Priority Score
    idea.calculate_rice_score()

    db.session.commit()

    return jsonify(idea.to_dict())


@rice_bp.route('/api/rice-ideas/<int:idea_id>', methods=['DELETE'])
def delete_rice_idea(idea_id):
    """Удалить Priority Score-идею"""
    idea = RiceIdea.query.get_or_404(idea_id)
    db.session.delete(idea)
    db.session.commit()
    return jsonify({'message': 'Priority Score idea deleted'}), 200


@rice_bp.route('/api/rice-ideas/<int:idea_id>/to-kanban', methods=['POST'])
def move_rice_idea_to_kanban(idea_id):
    """Перенести Priority Score-идею в Канбан"""
    idea = RiceIdea.query.get_or_404(idea_id)
    data = request.json

    # Создаём новую задачу из Priority Score-идеи
    task = Task(
        title=data.get('title', idea.title),
        description=data.get('description', idea.description),
        ideichnaya_link=data.get('ideichnaya_link'),
        assignee=data.get('assignee'),
        executor=data.get('executor'),
        priority=data.get('priority', 'Medium'),
        status=data.get('status', 'New'),
        rice_value=idea.value,
        rice_reach=idea.reach,
        rice_confidence=idea.confidence,
        budget_impact=idea.budget_impact,
        eisenhower_urgent=data.get('eisenhower_urgent', False),
        eisenhower_important=data.get('eisenhower_important', False)
    )

    # Добавляем теги
    tag_ids = data.get('tag_ids', [])
    if tag_ids:
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        task.tags = tags

    # Вычисляем Priority Score
    task.calculate_rice_score()

    db.session.add(task)

    # Удаляем Priority Score-идею после переноса
    db.session.delete(idea)

    db.session.commit()

    return jsonify(task.to_dict()), 201


# === Tasks with Priority Score API (для вкладки "Канбан" в Priority Score) ===

@rice_bp.route('/api/tasks-with-rice', methods=['GET'])
def get_tasks_with_rice():
    """Получить задачи из канбана с заполненными Priority Score-метриками (исключая Done)"""
    priority = request.args.get('priority')
    status = request.args.get('status')

    query = Task.query.filter(
        Task.rice_value.isnot(None),
        Task.rice_reach.isnot(None),
        Task.rice_confidence.isnot(None),
        Task.status != 'Done'  # Исключаем завершённые задачи
    )

    if priority:
        query = query.filter(Task.priority == priority)
    if status:
        query = query.filter(Task.status == status)

    # Сортируем по VRC Score (null в конце)
    tasks = query.order_by(Task.rice_score.desc().nullslast()).all()
    return jsonify([task.to_dict() for task in tasks])
