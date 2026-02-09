#!/bin/bash
# Скрипт для автоматического коммита и push всех изменений в GitHub

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  🔄 Синхронизация с GitHub                               ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"

# Переход в директорию проекта
cd "$(dirname "$0")"

# Проверка наличия локальных изменений
if [[ -n $(git status -s) ]]; then
    # Есть локальные изменения - коммитим их
    echo -e "\n${YELLOW}📝 Изменённые файлы:${NC}"
    git status -s

    echo -e "\n${YELLOW}➕ Добавляю изменения...${NC}"
    git add .

    COMMIT_MSG="Auto-sync: $(date '+%Y-%m-%d %H:%M:%S')"
    echo -e "${YELLOW}💾 Создаю коммит: ${COMMIT_MSG}${NC}"
    git commit -m "$COMMIT_MSG"
fi

# Теперь получаем изменения с GitHub
echo -e "\n${YELLOW}📥 Получаю изменения с GitHub...${NC}"
if git pull origin main --rebase; then
    echo -e "${GREEN}✅ Изменения с GitHub получены${NC}"
else
    echo -e "${RED}❌ Ошибка при получении изменений${NC}"
    echo -e "${YELLOW}💡 Возможно, есть конфликты. Разрешите их вручную:${NC}"
    echo -e "${YELLOW}   1. git status  # посмотреть конфликты${NC}"
    echo -e "${YELLOW}   2. Отредактируйте конфликтующие файлы${NC}"
    echo -e "${YELLOW}   3. git add .${NC}"
    echo -e "${YELLOW}   4. git rebase --continue${NC}"
    echo -e "${YELLOW}   5. ./s  # повторите синхронизацию${NC}"
    exit 1
fi

# Push в GitHub
echo -e "\n${YELLOW}📤 Отправляю изменения в GitHub...${NC}"
if git push origin main; then
    echo -e "\n${GREEN}✅ Успешно синхронизировано с GitHub!${NC}"
    echo -e "${GREEN}✅ Можете продолжить работу на другом компьютере${NC}"
else
    echo -e "\n${RED}❌ Ошибка при отправке в GitHub${NC}"
    echo -e "${YELLOW}💡 Попробуйте выполнить: git status${NC}"
    exit 1
fi

echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}\n"

