#!/bin/bash
# Скрипт для остановки автоматической синхронизации

PLIST_NAME="com.zadachnik.autosync.plist"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_NAME"

echo "🛑 Останавливаю автосинхронизацию..."

if launchctl list | grep -q "com.zadachnik.autosync"; then
    launchctl unload "$PLIST_DEST"
    echo "✅ Автосинхронизация остановлена"
    echo ""
    echo "💡 Для повторного запуска используйте:"
    echo "   ./setup_autosync.sh"
else
    echo "⚠️  Сервис не запущен"
fi

