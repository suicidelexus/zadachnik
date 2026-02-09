from flask import Blueprint, request, jsonify
from models import db, Task
import pandas as pd
from io import BytesIO

import_bp = Blueprint('import', __name__)

# Маппинг названий столбцов
COLUMN_MAPPING = {
    'название': 'title',
    'title': 'title',
    'ссылка': 'ideichnaya_link',
    'ссылка на идеичную': 'ideichnaya_link',
    'ideichnaya_link': 'ideichnaya_link',
    'описание': 'description',
    'description': 'description',
    'постановщик': 'assignee',
    'assignee': 'assignee',
    'исполнитель': 'executor',
    'executor': 'executor',
    'приоритет': 'priority',
    'priority': 'priority',
    'статус': 'status',
    'status': 'status',
}

# Допустимые значения приоритетов
PRIORITY_VALUES = ['Low', 'Medium', 'High', 'Highest']
PRIORITY_MAPPING = {
    'low': 'Low',
    'medium': 'Medium',
    'high': 'High',
    'highest': 'Highest',
}

# Допустимые значения статусов
STATUS_VALUES = ['New', 'Collecting', 'Ready for Dev', 'In Dev', 'Ready for Release', 'Done']
STATUS_MAPPING = {
    'new': 'New',
    'collecting': 'Collecting',
    'ready for dev': 'Ready for Dev',
    'in dev': 'In Dev',
    'ready for release': 'Ready for Release',
    'done': 'Done',
}

# Обязательные поля
REQUIRED_FIELDS = ['title', 'ideichnaya_link', 'description', 'assignee', 'executor', 'priority', 'status']


def normalize_column_name(col):
    """Нормализует название столбца"""
    return col.strip().lower()


def normalize_priority(value):
    """Нормализует значение приоритета"""
    if pd.isna(value) or value == '':
        return None
    value_lower = str(value).strip().lower()
    return PRIORITY_MAPPING.get(value_lower)


def normalize_status(value):
    """Нормализует значение статуса"""
    if pd.isna(value) or value == '':
        return 'New'
    value_lower = str(value).strip().lower()
    return STATUS_MAPPING.get(value_lower, 'New')


@import_bp.route('/api/import', methods=['POST'])
def import_tasks():
    """Импорт задач из Excel или CSV файла"""
    if 'file' not in request.files:
        return jsonify({'error': 'Файл не загружен'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Файл не выбран'}), 400

    filename = file.filename.lower()

    try:
        # Читаем файл в DataFrame
        if filename.endswith('.xlsx') or filename.endswith('.xls'):
            df = pd.read_excel(BytesIO(file.read()))
        elif filename.endswith('.csv'):
            df = pd.read_csv(BytesIO(file.read()), encoding='utf-8')
        else:
            return jsonify({'error': 'Неподдерживаемый формат файла. Используйте .xlsx или .csv'}), 400

        # Нормализуем названия столбцов
        df.columns = [normalize_column_name(col) for col in df.columns]

        # Маппим столбцы
        column_map = {}
        for col in df.columns:
            if col in COLUMN_MAPPING:
                column_map[col] = COLUMN_MAPPING[col]

        df = df.rename(columns=column_map)

        # Проверяем наличие обязательных полей
        missing_fields = []
        for field in REQUIRED_FIELDS:
            if field not in df.columns:
                # Пробуем найти альтернативное название
                found = False
                for orig_col, mapped_col in COLUMN_MAPPING.items():
                    if mapped_col == field and orig_col in df.columns:
                        found = True
                        break
                if not found:
                    missing_fields.append(field)

        if missing_fields:
            field_names = {
                'title': 'Название',
                'ideichnaya_link': 'Ссылка / Ссылка на идеичную',
                'description': 'Описание',
                'assignee': 'Постановщик',
                'executor': 'Исполнитель',
                'priority': 'Приоритет',
                'status': 'Статус'
            }
            missing_names = [field_names.get(f, f) for f in missing_fields]
            return jsonify({
                'error': f'Отсутствуют обязательные столбцы: {", ".join(missing_names)}'
            }), 400

        # Импортируем задачи
        imported_count = 0
        errors = []

        for index, row in df.iterrows():
            row_num = index + 2  # +2 потому что index начинается с 0, а строка 1 - заголовки

            try:
                # Проверяем обязательные поля
                title = str(row.get('title', '')).strip() if pd.notna(row.get('title')) else ''
                if not title:
                    errors.append(f'Строка {row_num}: пустое название')
                    continue

                # Нормализуем приоритет
                priority = normalize_priority(row.get('priority'))
                if priority is None:
                    errors.append(f'Строка {row_num}: некорректный приоритет "{row.get("priority")}"')
                    continue

                # Нормализуем статус
                status = normalize_status(row.get('status'))

                # Создаём задачу
                task = Task(
                    title=title,
                    ideichnaya_link=str(row.get('ideichnaya_link', '')).strip() if pd.notna(row.get('ideichnaya_link')) else None,
                    description=str(row.get('description', '')).strip() if pd.notna(row.get('description')) else None,
                    assignee=str(row.get('assignee', '')).strip() if pd.notna(row.get('assignee')) else None,
                    executor=str(row.get('executor', '')).strip() if pd.notna(row.get('executor')) else None,
                    priority=priority,
                    status=status
                )

                db.session.add(task)
                imported_count += 1

            except Exception as e:
                errors.append(f'Строка {row_num}: {str(e)}')

        db.session.commit()

        # Формируем отчёт
        result = {
            'success': True,
            'imported': imported_count,
            'total': len(df),
            'errors_count': len(errors),
            'errors': errors[:20]  # Показываем максимум 20 ошибок
        }

        if len(errors) > 20:
            result['errors'].append(f'... и ещё {len(errors) - 20} ошибок')

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': f'Ошибка обработки файла: {str(e)}'}), 400


@import_bp.route('/api/import/template', methods=['GET'])
def download_template():
    """Скачать шаблон для импорта"""
    from flask import Response
    import io

    # Создаём шаблон
    template_data = {
        'Название': ['Пример задачи 1', 'Пример задачи 2'],
        'Ссылка': ['https://example.com/task1', 'https://example.com/task2'],
        'Описание': ['Описание первой задачи', 'Описание второй задачи'],
        'Постановщик': ['Иван Иванов', 'Пётр Петров'],
        'Исполнитель': ['Сидор Сидоров', 'Алексей Алексеев'],
        'Приоритет': ['High', 'Medium'],
        'Статус': ['New', 'In Dev']
    }

    df = pd.DataFrame(template_data)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Задачи')
    output.seek(0)

    return Response(
        output.getvalue(),
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=import_template.xlsx'}
    )
