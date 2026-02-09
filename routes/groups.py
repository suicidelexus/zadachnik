"""
Routes для управления группами задач
"""
from flask import Blueprint, request, jsonify
from models import db, Group

groups_bp = Blueprint('groups', __name__)


@groups_bp.route('/api/groups', methods=['GET'])
def get_groups():
    """Получить все группы"""
    groups = Group.query.order_by(Group.created_at.desc()).all()
    return jsonify([group.to_dict() for group in groups])


@groups_bp.route('/api/groups/<int:group_id>', methods=['GET'])
def get_group(group_id):
    """Получить группу по ID"""
    group = Group.query.get_or_404(group_id)
    return jsonify(group.to_dict())


@groups_bp.route('/api/groups', methods=['POST'])
def create_group():
    """Создать новую группу"""
    data = request.json

    # Проверяем уникальность имени
    existing = Group.query.filter(Group.name.ilike(data.get('name'))).first()
    if existing:
        return jsonify({'error': 'Group with this name already exists'}), 400

    group = Group(
        name=data.get('name'),
        description=data.get('description'),
        color=data.get('color', '#6366f1'),
        icon=data.get('icon', '📁')
    )

    db.session.add(group)
    db.session.commit()

    return jsonify(group.to_dict()), 201


@groups_bp.route('/api/groups/<int:group_id>', methods=['PUT'])
def update_group(group_id):
    """Обновить группу"""
    group = Group.query.get_or_404(group_id)
    data = request.json

    group.name = data.get('name', group.name)
    group.description = data.get('description', group.description)
    group.color = data.get('color', group.color)
    group.icon = data.get('icon', group.icon)

    db.session.commit()

    return jsonify(group.to_dict())


@groups_bp.route('/api/groups/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    """Удалить группу"""
    group = Group.query.get_or_404(group_id)

    # Удаляем связь с задачами (устанавливаем group_id в NULL)
    from models import Task
    Task.query.filter_by(group_id=group_id).update({'group_id': None})

    db.session.delete(group)
    db.session.commit()

    return jsonify({'message': 'Group deleted'}), 200


@groups_bp.route('/api/groups/<int:group_id>/tasks', methods=['GET'])
def get_group_tasks(group_id):
    """Получить все задачи группы"""
    group = Group.query.get_or_404(group_id)
    return jsonify([task.to_dict() for task in group.tasks])
