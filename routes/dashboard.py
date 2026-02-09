from flask import Blueprint, request, jsonify
from models import db, Task

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/api/dashboard/stats', methods=['GET'])
def get_stats():
    """Получить статистику для дашборда"""
    priority = request.args.get('priority')
    status = request.args.get('status')
    tag_id = request.args.get('tag_id')

    # Базовый запрос
    query = Task.query

    if priority:
        query = query.filter(Task.priority == priority)
    if status:
        query = query.filter(Task.status == status)
    if tag_id:
        from models import Tag
        query = query.filter(Task.tags.any(Tag.id == int(tag_id)))

    tasks = query.all()

    # Общая статистика
    total_tasks = len(tasks)

    # По приоритетам
    priority_stats = {
        'Low': 0,
        'Medium': 0,
        'High': 0,
        'Highest': 0
    }
    for task in tasks:
        if task.priority in priority_stats:
            priority_stats[task.priority] += 1

    # По статусам
    status_stats = {
        'New': 0,
        'Collecting': 0,
        'Ready for Dev': 0,
        'In Dev': 0,
        'Ready for Release': 0,
        'Done': 0
    }
    for task in tasks:
        if task.status in status_stats:
            status_stats[task.status] += 1

    # По квадрантам Эйзенхауэра
    eisenhower_stats = {
        'quadrant_1': 0,  # Срочно и Важно
        'quadrant_2': 0,  # Не срочно, но Важно
        'quadrant_3': 0,  # Срочно, но Не важно
        'quadrant_4': 0   # Не срочно и Не важно
    }
    for task in tasks:
        quadrant = task.get_eisenhower_quadrant()
        eisenhower_stats[f'quadrant_{quadrant}'] += 1

    # Топ задач по VRC Score
    top_rice = sorted(
        [t for t in tasks if t.rice_score is not None],
        key=lambda x: x.rice_score or 0,
        reverse=True
    )[:5]

    # По тегам
    from models import Tag
    all_tags = Tag.query.all()
    tags_stats = {}
    for tag in all_tags:
        count = len([t for t in tasks if tag in t.tags])
        if count > 0:
            tags_stats[tag.name] = {
                'count': count,
                'color': tag.color
            }

    return jsonify({
        'total_tasks': total_tasks,
        'priority_stats': priority_stats,
        'status_stats': status_stats,
        'eisenhower_stats': eisenhower_stats,
        'top_rice_tasks': [t.to_dict() for t in top_rice],
        'tags_stats': tags_stats
    })
