#!/bin/bash
# Скрипт для проверки статуса автосинхронизации

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  📊 Статус автоматической синхронизации                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

if launchctl list | grep -q "com.zadachnik.autosync"; then
    echo "✅ Статус: ЗАПУЩЕН"
    echo ""
    echo "📝 Информация о сервисе:"
    launchctl list | grep "com.zadachnik.autosync"
    echo ""
    echo "📄 Логи:"
    echo "   Вывод:  /tmp/zadachnik-autosync.log"
    echo "   Ошибки: /tmp/zadachnik-autosync-error.log"
    echo ""
    echo "📖 Последние 10 строк лога:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    if [ -f "/tmp/zadachnik-autosync.log" ]; then
        tail -10 /tmp/zadachnik-autosync.log
    else
        echo "Лог пока пуст (сервис только запущен)"
    fi
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🔍 Посмотреть полный лог:"
    echo "   tail -f /tmp/zadachnik-autosync.log"
    echo ""
    echo "🛑 Остановить:"
    echo "   ./stop_autosync.sh"
else
    echo "❌ Статус: НЕ ЗАПУЩЕН"
    echo ""
    echo "🚀 Запустить автосинхронизацию:"
    echo "   ./setup_autosync.sh"
fi

