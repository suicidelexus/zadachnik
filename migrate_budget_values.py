"""
Миграция: Обновление значений budget_impact на новые коэффициенты
Старые: 0.7, 1.0, 1.3, 1.6, 2.0
Новые: 1.0, 1.2, 1.5, 2.0
"""
from main import app
from models import db

with app.app_context():
    # Маппинг старых значений на новые
    mapping = {
        0.7: 1.0,
        1.3: 1.2,
        1.6: 1.5,
        # 1.0 и 2.0 остаются без изменений
    }

    # Обновляем tasks
    for old_val, new_val in mapping.items():
        result = db.session.execute(
            db.text('UPDATE tasks SET budget_impact = :new_val WHERE budget_impact = :old_val'),
            {'old_val': old_val, 'new_val': new_val}
        )
        if result.rowcount > 0:
            print(f"✓ Tasks: {result.rowcount} записей обновлено {old_val} → {new_val}")

    # Обновляем rice_ideas
    for old_val, new_val in mapping.items():
        result = db.session.execute(
            db.text('UPDATE rice_ideas SET budget_impact = :new_val WHERE budget_impact = :old_val'),
            {'old_val': old_val, 'new_val': new_val}
        )
        if result.rowcount > 0:
            print(f"✓ RiceIdeas: {result.rowcount} записей обновлено {old_val} → {new_val}")

    db.session.commit()
    print("\n✅ Миграция значений Budget Impact завершена успешно!")
