from main import app, db
from models import Task, Tag

with app.app_context():
    # Создаём теги для тестирования
    tags_data = [
        {'name': 'Backend', 'color': '#3b82f6'},
        {'name': 'Frontend', 'color': '#22c55e'},
        {'name': 'Design', 'color': '#f59e0b'},
        {'name': 'Bug', 'color': '#ef4444'},
    ]

    tags = {}
    for tag_data in tags_data:
        existing = Tag.query.filter_by(name=tag_data['name']).first()
        if not existing:
            tag = Tag(name=tag_data['name'], color=tag_data['color'])
            db.session.add(tag)
            db.session.flush()
            tags[tag_data['name']] = tag
        else:
            tags[tag_data['name']] = existing

    # Тестовые задачи
    tasks_data = [
        {
            'title': 'Интеграция с платёжной системой',
            'ideichnaya_link': 'https://ideichnaya.ru/task/1001',
            'description': 'Необходимо интегрировать платёжный шлюз для обработки онлайн-платежей',
            'assignee': 'Петров Иван',
            'executor': 'Сидоров Алексей',
            'priority': 'Highest',
            'status': 'In Dev',
            'tags': ['Backend']
        },
        {
            'title': 'Редизайн главной страницы',
            'ideichnaya_link': 'https://ideichnaya.ru/task/1002',
            'description': 'Обновить UI главной страницы согласно новому дизайн-макету',
            'assignee': 'Козлова Мария',
            'executor': 'Николаев Дмитрий',
            'priority': 'High',
            'status': 'Ready for Dev',
            'tags': ['Frontend', 'Design']
        },
        {
            'title': 'Оптимизация запросов к БД',
            'ideichnaya_link': 'https://ideichnaya.ru/task/1003',
            'description': 'Ускорить медленные SQL-запросы в модуле отчётов',
            'assignee': 'Иванов Сергей',
            'executor': 'Петров Иван',
            'priority': 'High',
            'status': 'New',
            'tags': ['Backend']
        },
        {
            'title': 'Исправить баг в авторизации',
            'ideichnaya_link': 'https://ideichnaya.ru/task/1004',
            'description': 'При определённых условиях пользователь не может войти в систему',
            'assignee': 'Смирнова Анна',
            'executor': 'Сидоров Алексей',
            'priority': 'Highest',
            'status': 'In Dev',
            'tags': ['Backend', 'Bug']
        },
        {
            'title': 'Добавить тёмную тему',
            'ideichnaya_link': 'https://ideichnaya.ru/task/1005',
            'description': 'Реализовать переключение между светлой и тёмной темой',
            'assignee': 'Козлова Мария',
            'executor': 'Фёдоров Максим',
            'priority': 'Medium',
            'status': 'Collecting',
            'tags': ['Frontend', 'Design']
        },
        {
            'title': 'Документация API',
            'ideichnaya_link': 'https://ideichnaya.ru/task/1006',
            'description': 'Написать документацию для REST API с примерами запросов',
            'assignee': 'Иванов Сергей',
            'executor': 'Кузнецова Елена',
            'priority': 'Low',
            'status': 'New',
            'tags': []
        },
        {
            'title': 'Мобильная адаптация личного кабинета',
            'ideichnaya_link': 'https://ideichnaya.ru/task/1007',
            'description': 'Адаптировать все страницы личного кабинета для мобильных устройств',
            'assignee': 'Козлова Мария',
            'executor': 'Николаев Дмитрий',
            'priority': 'High',
            'status': 'Ready for Release',
            'tags': ['Frontend']
        },
        {
            'title': 'Кэширование данных Redis',
            'ideichnaya_link': 'https://ideichnaya.ru/task/1008',
            'description': 'Внедрить Redis для кэширования часто запрашиваемых данных',
            'assignee': 'Петров Иван',
            'executor': 'Сидоров Алексей',
            'priority': 'Medium',
            'status': 'In Dev',
            'tags': ['Backend']
        },
        {
            'title': 'Баг: неправильное отображение дат',
            'ideichnaya_link': 'https://ideichnaya.ru/task/1009',
            'description': 'Даты отображаются в неправильном формате для некоторых локалей',
            'assignee': 'Смирнова Анна',
            'executor': 'Фёдоров Максим',
            'priority': 'Low',
            'status': 'New',
            'tags': ['Frontend', 'Bug']
        },
        {
            'title': 'Экспорт отчётов в PDF',
            'ideichnaya_link': 'https://ideichnaya.ru/task/1010',
            'description': 'Добавить возможность экспорта любого отчёта в формат PDF',
            'assignee': 'Иванов Сергей',
            'executor': 'Кузнецова Елена',
            'priority': 'Medium',
            'status': 'Collecting',
            'tags': ['Backend', 'Frontend']
        },
    ]

    for task_data in tasks_data:
        task = Task(
            title=task_data['title'],
            ideichnaya_link=task_data['ideichnaya_link'],
            description=task_data['description'],
            assignee=task_data['assignee'],
            executor=task_data['executor'],
            priority=task_data['priority'],
            status=task_data['status']
        )

        # Добавляем теги
        for tag_name in task_data['tags']:
            if tag_name in tags:
                task.tags.append(tags[tag_name])

        db.session.add(task)

    db.session.commit()

    count = Task.query.count()
    print(f'✅ Создано 10 тестовых задач!')
    print(f'Всего задач в базе: {count}')
