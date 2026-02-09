from flask import Blueprint, request, jsonify, current_app, send_from_directory
from models import db, Task, Tag, Comment, Attachment
from werkzeug.utils import secure_filename
import os
import uuid

tasks_bp = Blueprint('tasks', __name__)

PRIORITIES = ['Low', 'Medium', 'High', 'Highest']
STATUSES = ['New', 'Collecting', 'Ready for Dev', 'In Dev', 'Ready for Release', 'Done']

# Разрешённые расширения файлов
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt', 'zip', 'rar', 'csv'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@tasks_bp.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Получить все задачи с фильтрацией"""
    priority = request.args.get('priority')
    status = request.args.get('status')
    tag_id = request.args.get('tag_id')
    search = request.args.get('search')
    include_done = request.args.get('include_done', 'false').lower() == 'true'

    query = Task.query

    # По умолчанию исключаем задачи со статусом Done
    if not include_done and not status:
        query = query.filter(Task.status != 'Done')

    if priority:
        query = query.filter(Task.priority == priority)
    if status:
        query = query.filter(Task.status == status)
    if tag_id:
        query = query.filter(Task.tags.any(Tag.id == int(tag_id)))
    if search:
        query = query.filter(
            db.or_(
                Task.title.ilike(f'%{search}%'),
                Task.description.ilike(f'%{search}%')
            )
        )

    tasks = query.order_by(Task.created_at.desc()).all()
    return jsonify([task.to_dict() for task in tasks])


@tasks_bp.route('/api/tasks', methods=['POST'])
def create_task():
    """Создать новую задачу"""
    data = request.json

    task = Task(
        title=data.get('title'),
        ideichnaya_link=data.get('ideichnaya_link'),
        description=data.get('description'),
        assignee=data.get('assignee'),
        executor=data.get('executor'),
        priority=data.get('priority', 'Medium'),
        status=data.get('status', 'New'),
        rice_value=data.get('rice_value'),
        rice_reach=data.get('rice_reach'),
        rice_confidence=data.get('rice_confidence'),
        budget_impact=data.get('budget_impact', 1.0),
        eisenhower_urgent=data.get('eisenhower_urgent', False),
        eisenhower_important=data.get('eisenhower_important', False),
        group_id=data.get('group_id')
    )

    # Добавляем теги
    tag_ids = data.get('tag_ids', [])
    if tag_ids:
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        task.tags = tags

    # Вычисляем Priority Score
    task.calculate_rice_score()

    db.session.add(task)
    db.session.commit()

    return jsonify(task.to_dict()), 201


@tasks_bp.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Получить задачу по ID"""
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict())


@tasks_bp.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Обновить задачу"""
    task = Task.query.get_or_404(task_id)
    data = request.json

    task.title = data.get('title', task.title)
    task.ideichnaya_link = data.get('ideichnaya_link', task.ideichnaya_link)
    task.description = data.get('description', task.description)
    task.assignee = data.get('assignee', task.assignee)
    task.executor = data.get('executor', task.executor)
    task.priority = data.get('priority', task.priority)
    task.status = data.get('status', task.status)
    task.rice_value = data.get('rice_value', task.rice_value)
    task.rice_reach = data.get('rice_reach', task.rice_reach)
    task.rice_confidence = data.get('rice_confidence', task.rice_confidence)
    task.budget_impact = data.get('budget_impact', task.budget_impact)
    task.eisenhower_urgent = data.get('eisenhower_urgent', task.eisenhower_urgent)
    task.eisenhower_important = data.get('eisenhower_important', task.eisenhower_important)

    # Обновляем группу
    if 'group_id' in data:
        task.group_id = data['group_id'] if data['group_id'] else None

    # Обновляем теги
    if 'tag_ids' in data:
        tags = Tag.query.filter(Tag.id.in_(data['tag_ids'])).all()
        task.tags = tags

    # Пересчитываем Priority Score
    task.calculate_rice_score()

    db.session.commit()

    return jsonify(task.to_dict())


@tasks_bp.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Удалить задачу"""
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'}), 200


@tasks_bp.route('/api/tasks/<int:task_id>/priority', methods=['PATCH'])
def update_task_priority(task_id):
    """Обновить приоритет задачи (для drag-and-drop)"""
    task = Task.query.get_or_404(task_id)
    data = request.json
    task.priority = data.get('priority', task.priority)
    db.session.commit()
    return jsonify(task.to_dict())


@tasks_bp.route('/api/tasks/<int:task_id>/status', methods=['PATCH'])
def update_task_status(task_id):
    """Обновить статус задачи"""
    task = Task.query.get_or_404(task_id)
    data = request.json
    task.status = data.get('status', task.status)
    db.session.commit()
    return jsonify(task.to_dict())


# Комментарии
@tasks_bp.route('/api/tasks/<int:task_id>/comments', methods=['POST'])
def add_comment(task_id):
    """Добавить комментарий к задаче"""
    task = Task.query.get_or_404(task_id)
    data = request.json

    comment = Comment(
        task_id=task_id,
        text=data.get('text'),
        author=data.get('author')
    )

    db.session.add(comment)
    db.session.commit()

    return jsonify(comment.to_dict()), 201


@tasks_bp.route('/api/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    """Удалить комментарий"""
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted'}), 200


@tasks_bp.route('/api/priorities', methods=['GET'])
def get_priorities():
    """Получить список приоритетов"""
    return jsonify(PRIORITIES)


@tasks_bp.route('/api/statuses', methods=['GET'])
def get_statuses():
    """Получить список статусов"""
    return jsonify(STATUSES)


# ======================= ВЛОЖЕНИЯ (Attachments) =======================

@tasks_bp.route('/api/tasks/<int:task_id>/attachments', methods=['GET'])
def get_attachments(task_id):
    """Получить вложения задачи"""
    task = Task.query.get_or_404(task_id)
    return jsonify([att.to_dict() for att in task.attachments])


@tasks_bp.route('/api/tasks/<int:task_id>/attachments', methods=['POST'])
def upload_attachment(task_id):
    """Загрузить вложение к задаче"""
    task = Task.query.get_or_404(task_id)

    if 'file' not in request.files:
        return jsonify({'error': 'Файл не выбран'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'Файл не выбран'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Недопустимый тип файла'}), 400

    # Проверяем размер файла
    file.seek(0, 2)  # Перемещаемся в конец файла
    file_size = file.tell()
    file.seek(0)  # Возвращаемся в начало

    if file_size > MAX_FILE_SIZE:
        return jsonify({'error': 'Файл слишком большой (макс. 16MB)'}), 400

    # Генерируем уникальное имя файла
    original_name = secure_filename(file.filename)
    ext = original_name.rsplit('.', 1)[1].lower() if '.' in original_name else ''
    filename = f"{uuid.uuid4().hex}.{ext}" if ext else uuid.uuid4().hex

    # Создаём папку для загрузок если её нет
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)

    # Сохраняем файл
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    # Создаём запись в БД
    attachment = Attachment(
        task_id=task_id,
        filename=filename,
        original_name=original_name,
        file_size=file_size,
        mime_type=file.content_type
    )

    db.session.add(attachment)
    db.session.commit()

    return jsonify(attachment.to_dict()), 201


@tasks_bp.route('/api/attachments/<int:attachment_id>', methods=['GET'])
def get_attachment(attachment_id):
    """Получить информацию о вложении"""
    attachment = Attachment.query.get_or_404(attachment_id)
    return jsonify(attachment.to_dict())


@tasks_bp.route('/api/attachments/<int:attachment_id>', methods=['DELETE'])
def delete_attachment(attachment_id):
    """Удалить вложение"""
    attachment = Attachment.query.get_or_404(attachment_id)

    # Удаляем файл с диска
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
    filepath = os.path.join(upload_folder, attachment.filename)

    if os.path.exists(filepath):
        os.remove(filepath)

    db.session.delete(attachment)
    db.session.commit()

    return jsonify({'message': 'Attachment deleted'}), 200


@tasks_bp.route('/api/attachments/<int:attachment_id>/download', methods=['GET'])
def download_attachment(attachment_id):
    """Скачать вложение"""
    attachment = Attachment.query.get_or_404(attachment_id)
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')

    return send_from_directory(
        upload_folder,
        attachment.filename,
        as_attachment=True,
        download_name=attachment.original_name
    )

