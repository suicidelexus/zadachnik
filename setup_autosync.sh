#!/bin/bash
# Скрипт для настройки автоматической синхронизации с GitHub
# Запускается при входе в систему и работает постоянно в фоне

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLIST_NAME="com.zadachnik.autosync.plist"
PLIST_SOURCE="$SCRIPT_DIR/$PLIST_NAME"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_NAME"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  🚀 Установка автоматической синхронизации с GitHub         ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Проверка, что мы в нужной директории
if [ ! -f "$SCRIPT_DIR/auto_sync.py" ]; then
    echo "❌ Ошибка: Запустите скрипт из директории проекта zadachnik"
    exit 1
fi

# Создаём директорию LaunchAgents если её нет
mkdir -p "$HOME/Library/LaunchAgents"

# Останавливаем сервис если он уже запущен
if launchctl list | grep -q "com.zadachnik.autosync"; then
    echo "🛑 Останавливаю существующий сервис..."
    launchctl unload "$PLIST_DEST" 2>/dev/null || true
fi

# Копируем plist файл
echo "📄 Копирую конфигурационный файл..."
cp "$PLIST_SOURCE" "$PLIST_DEST"

# Загружаем сервис
echo "🔄 Запускаю сервис автосинхронизации..."
launchctl load "$PLIST_DEST"

# Проверяем статус
sleep 2
if launchctl list | grep -q "com.zadachnik.autosync"; then
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║  ✅ УСПЕШНО! Автосинхронизация настроена                    ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "📊 Что это означает:"
    echo "   • Сервис запущен и работает в фоне"
    echo "   • Автоматически проверяет изменения каждые 30 секунд"
    echo "   • Автоматически делает commit + push в GitHub"
    echo "   • Запускается автоматически при входе в систему"
    echo ""
    echo "📝 Логи сервиса:"
    echo "   Вывод:    /tmp/zadachnik-autosync.log"
    echo "   Ошибки:   /tmp/zadachnik-autosync-error.log"
    echo ""
    echo "🔍 Посмотреть логи:"
    echo "   tail -f /tmp/zadachnik-autosync.log"
    echo ""
    echo "🛑 Остановить автосинхронизацию:"
    echo "   ./stop_autosync.sh"
    echo ""
    echo "🔄 Перезапустить:"
    echo "   ./restart_autosync.sh"
    echo ""
    echo "🎉 Теперь все изменения автоматически отправляются в GitHub!"
    echo ""
else
    echo ""
    echo "❌ Не удалось запустить сервис"
    echo "Проверьте логи: cat /tmp/zadachnik-autosync-error.log"
    exit 1
fi

