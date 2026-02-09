from flask import Blueprint, request, jsonify
from models import db, Task

done_bp = Blueprint('done', __name__)


@done_bp.route('/api/tasks/done', methods=['GET'])
def get_done_tasks():
    """Получить все завершённые задачи"""
    tasks = Task.query.filter(Task.status == 'Done').order_by(Task.updated_at.desc()).all()
    return jsonify([task.to_dict() for task in tasks])


@done_bp.route('/api/tasks/done/delete-all', methods=['DELETE'])
def delete_all_done_tasks():
    """Удалить все завершённые задачи"""
    Task.query.filter(Task.status == 'Done').delete()
    db.session.commit()
    return jsonify({'message': 'All done tasks deleted'}), 200


@done_bp.route('/api/tasks/<int:task_id>/restore', methods=['PATCH'])
def restore_task(task_id):
    """Вернуть задачу из Done в указанный статус"""
    task = Task.query.get_or_404(task_id)
    data = request.json
    task.status = data.get('status', 'New')
    db.session.commit()
    return jsonify(task.to_dict())
