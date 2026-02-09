#!/usr/bin/env python3
"""
Скрипт для автоматического коммита и push всех изменений в GitHub
Использование: python sync_github.py [сообщение коммита]
"""

import subprocess
import sys
from datetime import datetime

def run_command(command):
    """Выполняет команду и возвращает результат"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка: {e.stderr}")
        return None

def main():
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║  🔄 Синхронизация с GitHub                               ║")
    print("╚═══════════════════════════════════════════════════════════╝")

    # Проверка наличия локальных изменений
    status = run_command("git status -s")
    if status and status.strip() != "":
        # Есть локальные изменения - коммитим их сначала
        print("\n📝 Изменённые файлы:")
        print(status)

        print("➕ Добавляю изменения...")
        if run_command("git add .") is None:
            return 1

        # Создаём коммит
        if len(sys.argv) > 1:
            commit_msg = " ".join(sys.argv[1:])
        else:
            commit_msg = f"Auto-sync: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        print(f"💾 Создаю коммит: {commit_msg}")
        if run_command(f'git commit -m "{commit_msg}"') is None:
            return 1

    # Получаем изменения с GitHub
    print("\n📥 Получаю изменения с GitHub...")
    if run_command("git pull origin main --rebase") is None:
        print("❌ Ошибка при получении изменений")
        print("💡 Возможно, есть конфликты. Разрешите их вручную:")
        print("   1. git status  # посмотреть конфликты")
        print("   2. Отредактируйте конфликтующие файлы")
        print("   3. git add .")
        print("   4. git rebase --continue")
        print("   5. ./s  # повторите синхронизацию")
        return 1
    print("✅ Изменения с GitHub получены")

    # Push в GitHub
    print("\n📤 Отправляю изменения в GitHub...")
    if run_command("git push origin main") is None:
        print("❌ Ошибка при отправке")
        print("💡 Попробуйте: git status")
        return 1

    print("\n✅ Успешно синхронизировано с GitHub!")
    print("✅ Можете продолжить работу на другом компьютере")
    print("╚═══════════════════════════════════════════════════════════╝\n")
    return 0

if __name__ == "__main__":
    sys.exit(main())

