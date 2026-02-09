from flask import Blueprint, request, jsonify, Response
from models import db, Task, Tag
import io
import csv

export_bp = Blueprint('export', __name__)


@export_bp.route('/api/export/csv', methods=['GET'])
def export_csv():
    """Экспорт задач в CSV с учётом фильтров"""
    priority = request.args.get('priority')
    status = request.args.get('status')
    tag_id = request.args.get('tag_id')

    query = Task.query

    if priority:
        query = query.filter(Task.priority == priority)
    if status:
        query = query.filter(Task.status == status)
    if tag_id:
        query = query.filter(Task.tags.any(Tag.id == int(tag_id)))

    tasks = query.order_by(Task.created_at.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)

    # Заголовки
    writer.writerow([
        'ID', 'Название', 'Ссылка на Идеичную', 'Описание',
        'Постановщик', 'Исполнитель', 'Приоритет', 'Статус',
        'Priority Value', 'Priority Reach', 'Priority Confidence', 'Budget Impact', 'Priority Score',
        'Срочно', 'Важно', 'Квадрант Эйзенхауэра',
        'Теги', 'Создано', 'Обновлено'
    ])

    for task in tasks:
        quadrant_names = {
            1: 'Сделать сейчас',
            2: 'Запланировать',
            3: 'Делегировать',
            4: 'Удалить/Отложить'
        }

        writer.writerow([
            task.id,
            task.title,
            task.ideichnaya_link or '',
            task.description or '',
            task.assignee or '',
            task.executor or '',
            task.priority,
            task.status,
            task.rice_value or '',
            task.rice_reach or '',
            task.rice_confidence or '',
            task.budget_impact or '',
            round(task.rice_score, 2) if task.rice_score else '',
            'Да' if task.eisenhower_urgent else 'Нет',
            'Да' if task.eisenhower_important else 'Нет',
            quadrant_names.get(task.get_eisenhower_quadrant(), ''),
            ', '.join([tag.name for tag in task.tags]),
            task.created_at.strftime('%Y-%m-%d %H:%M') if task.created_at else '',
            task.updated_at.strftime('%Y-%m-%d %H:%M') if task.updated_at else ''
        ])

    output.seek(0)

    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=tasks_export.csv'}
    )


@export_bp.route('/api/export/excel', methods=['GET'])
def export_excel():
    """Экспорт задач в Excel с учётом фильтров"""
    import pandas as pd
    from io import BytesIO

    priority = request.args.get('priority')
    status = request.args.get('status')
    tag_id = request.args.get('tag_id')

    query = Task.query

    if priority:
        query = query.filter(Task.priority == priority)
    if status:
        query = query.filter(Task.status == status)
    if tag_id:
        query = query.filter(Task.tags.any(Tag.id == int(tag_id)))

    tasks = query.order_by(Task.created_at.desc()).all()

    quadrant_names = {
        1: 'Сделать сейчас',
        2: 'Запланировать',
        3: 'Делегировать',
        4: 'Удалить/Отложить'
    }

    data = []
    for task in tasks:
        data.append({
            'ID': task.id,
            'Название': task.title,
            'Ссылка на Идеичную': task.ideichnaya_link or '',
            'Описание': task.description or '',
            'Постановщик': task.assignee or '',
            'Исполнитель': task.executor or '',
            'Приоритет': task.priority,
            'Статус': task.status,
            'Priority Value': task.rice_value or '',
            'Priority Reach': task.rice_reach or '',
            'Priority Confidence': task.rice_confidence or '',
            'Budget Impact': task.budget_impact or '',
            'Priority Score': round(task.rice_score, 2) if task.rice_score else '',
            'Срочно': 'Да' if task.eisenhower_urgent else 'Нет',
            'Важно': 'Да' if task.eisenhower_important else 'Нет',
            'Квадрант Эйзенхауэра': quadrant_names.get(task.get_eisenhower_quadrant(), ''),
            'Теги': ', '.join([tag.name for tag in task.tags]),
            'Создано': task.created_at.strftime('%Y-%m-%d %H:%M') if task.created_at else '',
            'Обновлено': task.updated_at.strftime('%Y-%m-%d %H:%M') if task.updated_at else ''
        })

    df = pd.DataFrame(data)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Задачи')

    output.seek(0)

    return Response(
        output.getvalue(),
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=tasks_export.xlsx'}
    )
