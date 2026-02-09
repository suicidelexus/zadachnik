#!/usr/bin/env python3
"""
Автоматическая синхронизация с GitHub по расписанию.
Запускается один раз в сутки в 18:00.

Использование:
    python auto_sync_daily.py

Остановка:
    Ctrl+C
"""

import os
import sys
import time
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# Настройки
WATCH_DIR = Path(__file__).parent.absolute()
SYNC_TIME = "18:00"  # Время синхронизации (24-часовой формат)

def run_command(command, capture=True):
    """Выполняет команду и возвращает результат"""
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
    print(f"\n{'='*60}")
    print(f"🔄 Ежедневная синхронизация - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")

    # Сначала получаем изменения с GitHub
    print("\n📥 Получаю изменения с GitHub...")
    if run_command("git pull origin main --rebase") is None:
        print("⚠️  Ошибка при получении изменений")
    else:
        print("✅ Изменения с GitHub получены")

    # Проверяем локальные изменения
    if not has_changes():
        print("\n✅ Нет локальных изменений для отправки")
        print(f"{'='*60}\n")
        return True

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
    commit_msg = f"Daily auto-sync: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
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

def get_next_sync_time():
    """Вычисляет следующее время синхронизации"""
    now = datetime.now()
    hour, minute = map(int, SYNC_TIME.split(':'))

    # Следующее время синхронизации сегодня
    next_sync = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

    # Если уже прошло сегодня, берём завтра
    if next_sync <= now:
        next_sync += timedelta(days=1)

    return next_sync

def seconds_until_next_sync():
    """Возвращает количество секунд до следующей синхронизации"""
    next_sync = get_next_sync_time()
    now = datetime.now()
    return (next_sync - now).total_seconds()

def main():
    """Главная функция"""
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║  🔄 Ежедневная авто-синхронизация с GitHub               ║
╚═══════════════════════════════════════════════════════════╝

📂 Директория: {WATCH_DIR}
⏰ Время синхронизации: {SYNC_TIME} (каждый день)
🛑 Остановка: Ctrl+C

Запускаю сервис...
""")

    # Выполняем синхронизацию сразу при запуске
    print("🚀 Выполняю начальную синхронизацию...")
    sync_to_github()

    try:
        while True:
            next_sync = get_next_sync_time()
            seconds = seconds_until_next_sync()

            print(f"⏳ Следующая синхронизация: {next_sync.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   (через {int(seconds/3600)} часов {int((seconds%3600)/60)} минут)")
            print(f"   Ожидание... (нажмите Ctrl+C для остановки)")

            # Спим до следующей синхронизации
            # Просыпаемся каждые 60 секунд для проверки
            while seconds > 0:
                sleep_time = min(60, seconds)
                time.sleep(sleep_time)
                seconds = seconds_until_next_sync()

                # Проверяем не пора ли синхронизироваться
                if seconds <= 0:
                    break

            # Выполняем синхронизацию
            sync_to_github()

    except KeyboardInterrupt:
        print("\n\n🛑 Остановка ежедневной синхронизации...")

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

