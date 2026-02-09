#!/usr/bin/env python3
"""
Автоматическая синхронизация с GitHub при изменении файлов.
Следит за изменениями и автоматически делает commit + push.

Использование:
    python auto_sync.py

Остановка:
    Ctrl+C
"""

import os
import sys
import time
import subprocess
from datetime import datetime
from pathlib import Path

# Настройки
WATCH_DIR = Path(__file__).parent.absolute()
SYNC_INTERVAL = 30  # Интервал проверки изменений (в секундах) - можно уменьшить до 10
IGNORE_PATTERNS = [
    '.git',
    '__pycache__',
    '*.pyc',
    '*.log',
    'instance',
    '.DS_Store',
    '.idea',
    'venv',
    'env',
    '*.db',
    'backup_*',
]

def run_command(command, capture=True):
    """Выполняет команду в shell"""
    try:
        if capture:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
                cwd=WATCH_DIR
            )
            return result.stdout.strip()
        else:
            subprocess.run(command, shell=True, check=True, cwd=WATCH_DIR)
            return None
    except subprocess.CalledProcessError as e:
        return None

def has_changes():
    """Проверяет наличие изменений в репозитории"""
    status = run_command("git status --porcelain")
    return status and status.strip() != ""

def sync_to_github():
    """Синхронизирует изменения с GitHub"""
    if not has_changes():
        return False

    print(f"\n{'='*60}")
    print(f"🔄 Обнаружены изменения - {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*60}")

    # Показываем что изменилось
    status = run_command("git status -s")
    if status:
        print("\n📝 Изменённые файлы:")
        for line in status.split('\n'):
            print(f"   {line}")

    # Добавляем все изменения
    print("\n➕ Добавляю изменения...")
    run_command("git add .", capture=False)

    # Создаём коммит
    commit_msg = f"Auto-sync: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    print(f"💾 Создаю коммит: {commit_msg}")
    run_command(f'git commit -m "{commit_msg}"', capture=False)

    # Пушим в GitHub
    print("📤 Отправляю в GitHub...")
    result = run_command("git push origin main")

    if result is not None or run_command("git status") is not None:
        print("✅ Успешно синхронизировано с GitHub!")
        print(f"{'='*60}\n")
        return True
    else:
        print("⚠️  Не удалось отправить в GitHub (проверьте подключение)")
        print(f"{'='*60}\n")
        return False

def main():
    """Главная функция"""
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║  🔄 Auto-Sync для Self's Product Board                   ║
╚═══════════════════════════════════════════════════════════╝

📂 Отслеживаемая директория: {WATCH_DIR}
⏱️  Интервал проверки: {SYNC_INTERVAL} сек
🛑 Остановка: Ctrl+C

Запускаю мониторинг изменений...
""")

    last_sync_time = time.time()

    try:
        while True:
            current_time = time.time()

            # Проверяем изменения каждые SYNC_INTERVAL секунд
            if current_time - last_sync_time >= SYNC_INTERVAL:
                if has_changes():
                    sync_to_github()
                else:
                    print(f"✓ Нет изменений - {datetime.now().strftime('%H:%M:%S')}", end='\r')

                last_sync_time = current_time

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\n🛑 Остановка автоматической синхронизации...")

        # Проверяем, есть ли несохранённые изменения
        if has_changes():
            print("\n⚠️  Обнаружены несохранённые изменения!")
            response = input("Синхронизировать перед выходом? (y/n): ")
            if response.lower() in ['y', 'yes', 'д', 'да']:
                sync_to_github()

        print("\n✅ Программа завершена")
        sys.exit(0)

if __name__ == "__main__":
    # Проверяем, что мы в git репозитории
    if not (WATCH_DIR / '.git').exists():
        print("❌ Ошибка: Это не Git репозиторий!")
        sys.exit(1)

    main()

