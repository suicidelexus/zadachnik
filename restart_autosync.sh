#!/bin/bash
# Скрипт для перезапуска автоматической синхронизации

PLIST_NAME="com.zadachnik.autosync.plist"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_NAME"

echo "🔄 Перезапускаю автосинхронизацию..."

# Останавливаем если запущен
if launchctl list | grep -q "com.zadachnik.autosync"; then
    launchctl unload "$PLIST_DEST" 2>/dev/null
    sleep 1
fi

# Запускаем снова
launchctl load "$PLIST_DEST"
sleep 2

# Проверяем статус
if launchctl list | grep -q "com.zadachnik.autosync"; then
    echo "✅ Автосинхронизация перезапущена"
    echo ""
    echo "📝 Посмотреть логи:"
    echo "   tail -f /tmp/zadachnik-autosync.log"
else
    echo "❌ Не удалось перезапустить"
    echo "Попробуйте: ./setup_autosync.sh"
fi

