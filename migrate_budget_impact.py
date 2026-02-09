"""
Миграция: Добавление поля budget_impact в таблицы tasks и rice_ideas
"""
from main import app
from models import db

with app.app_context():
    # Добавляем колонку budget_impact в обе таблицы
    try:
        # Для SQLite используем прямой SQL
        db.session.execute(db.text('ALTER TABLE tasks ADD COLUMN budget_impact FLOAT DEFAULT 1.0'))
        print("✓ Добавлена колонка budget_impact в таблицу tasks")
    except Exception as e:
        print(f"Колонка budget_impact уже существует в tasks или ошибка: {e}")

    try:
        db.session.execute(db.text('ALTER TABLE rice_ideas ADD COLUMN budget_impact FLOAT DEFAULT 1.0'))
        print("✓ Добавлена колонка budget_impact в таблицу rice_ideas")
    except Exception as e:
        print(f"Колонка budget_impact уже существует в rice_ideas или ошибка: {e}")

    db.session.commit()
    print("\n✅ Миграция завершена успешно!")
