// Global variables
let currentTaskId = null;
let allTags = [];

// Toast Notification
function showNotification(message, type = 'success') {
    // Удаляем предыдущее уведомление если есть
    const existingToast = document.querySelector('.toast-notification');
    if (existingToast) {
        existingToast.remove();
    }

    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    toast.innerHTML = `
        <span class="material-icons-round">${type === 'success' ? 'check_circle' : 'error'}</span>
        <span>${message}</span>
    `;

    document.body.appendChild(toast);

    // Анимация появления
    setTimeout(() => toast.classList.add('show'), 10);

    // Автоматическое скрытие через 3 секунды
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Submenu Toggle
function toggleSubmenu(element) {
    const parentItem = element.closest('.nav-parent');
    if (parentItem) {
        parentItem.classList.toggle('expanded');
    }
}

// Theme Toggle
function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', newTheme);

    const icon = document.getElementById('theme-icon');
    icon.textContent = newTheme === 'dark' ? 'light_mode' : 'dark_mode';

    localStorage.setItem('theme', newTheme);
}

// Load saved theme
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    const icon = document.getElementById('theme-icon');
    if (icon) {
        icon.textContent = savedTheme === 'dark' ? 'light_mode' : 'dark_mode';
    }

    // Load tags for forms
    loadTags();
});

// Tags Management
async function loadTags() {
    try {
        const response = await fetch('/api/tags');
        allTags = await response.json();
        updateTagsContainer();
    } catch (error) {
        console.error('Error loading tags:', error);
    }
}

function updateTagsContainer() {
    const container = document.getElementById('tagsContainer');
    if (!container) return;

    container.innerHTML = allTags.map(tag => `
        <input type="checkbox" id="tag-${tag.id}" class="tag-checkbox" value="${tag.id}">
        <label for="tag-${tag.id}" class="tag-label" style="background-color: ${tag.color}">${tag.name}</label>
    `).join('');
}

// Modal Functions
async function openModal(taskId = null) {
    const modal = document.getElementById('taskModal');
    const form = document.getElementById('taskForm');
    const title = document.getElementById('modalTitle');

    form.reset();
    document.getElementById('taskId').value = '';

    // Сначала загружаем теги и ждём завершения
    await loadTags();

    // Reset tag checkboxes
    document.querySelectorAll('.tag-checkbox').forEach(cb => cb.checked = false);

    // Сброс radio-кнопок матрицы Эйзенхауэра
    document.querySelectorAll('input[name="eisenhower_importance"]').forEach(el => el.checked = false);
    document.querySelectorAll('input[name="eisenhower_urgency"]').forEach(el => el.checked = false);
    const errorEl = document.getElementById('eisenhowerError');
    if (errorEl) errorEl.style.display = 'none';

    if (taskId) {
        title.textContent = 'Редактировать задачу';
        await loadTaskForEdit(taskId);
    } else {
        title.textContent = 'Новая задача';
    }

    // Поддержка как старых модалок, так и DaisyUI dialog
    if (modal.tagName === 'DIALOG') {
        modal.showModal();
    } else {
        modal.classList.add('active');
    }
}

function closeModal() {
    const modal = document.getElementById('taskModal');
    if (modal) {
        // Поддержка как старых модалок, так и DaisyUI dialog
        if (modal.tagName === 'DIALOG') {
            modal.close();
        } else {
            modal.classList.remove('active');
            modal.style.display = 'none';
            // Возвращаем display через небольшую задержку для следующего открытия
            setTimeout(() => {
                modal.style.display = '';
            }, 100);
        }
    }
}

async function loadTaskForEdit(taskId) {
    try {
        const response = await fetch(`/api/tasks/${taskId}`);
        const task = await response.json();

        document.getElementById('taskId').value = task.id;
        document.getElementById('title').value = task.title || '';
        document.getElementById('ideichnaya_link').value = task.ideichnaya_link || '';
        document.getElementById('description').value = task.description || '';
        document.getElementById('assignee').value = task.assignee || '';
        document.getElementById('executor').value = task.executor || '';
        document.getElementById('priority').value = task.priority;
        document.getElementById('status').value = task.status;
        document.getElementById('rice_value').value = task.rice_value || '';
        document.getElementById('rice_reach').value = task.rice_reach || '';
        document.getElementById('rice_confidence').value = task.rice_confidence ?? '';
        document.getElementById('budget_impact').value = task.budget_impact || '1.0';

        // Сброс radio-кнопок матрицы Эйзенхауэра
        document.querySelectorAll('input[name="eisenhower_importance"]').forEach(el => el.checked = false);
        document.querySelectorAll('input[name="eisenhower_urgency"]').forEach(el => el.checked = false);

        // Установка значений матрицы Эйзенхауэра
        if (task.eisenhower_important === true) {
            const radio = document.querySelector('input[name="eisenhower_importance"][value="important"]');
            if (radio) radio.checked = true;
        } else if (task.eisenhower_important === false) {
            const radio = document.querySelector('input[name="eisenhower_importance"][value="not_important"]');
            if (radio) radio.checked = true;
        }

        if (task.eisenhower_urgent === true) {
            const radio = document.querySelector('input[name="eisenhower_urgency"][value="urgent"]');
            if (radio) radio.checked = true;
        } else if (task.eisenhower_urgent === false) {
            const radio = document.querySelector('input[name="eisenhower_urgency"][value="not_urgent"]');
            if (radio) radio.checked = true;
        }

        // Set tags
        task.tags.forEach(tag => {
            const checkbox = document.getElementById(`tag-${tag.id}`);
            if (checkbox) checkbox.checked = true;
        });
    } catch (error) {
        console.error('Error loading task:', error);
    }
}

// Валидация матрицы Эйзенхауэра
function validateEisenhower() {
    const importance = document.querySelector('input[name="eisenhower_importance"]:checked');
    const urgency = document.querySelector('input[name="eisenhower_urgency"]:checked');
    const errorEl = document.getElementById('eisenhowerError');

    // Оба пустые - ОК
    if (!importance && !urgency) {
        if (errorEl) errorEl.style.display = 'none';
        return true;
    }

    // Оба заполнены - ОК
    if (importance && urgency) {
        if (errorEl) errorEl.style.display = 'none';
        return true;
    }

    // Только один заполнен - ошибка
    if (errorEl) errorEl.style.display = 'block';
    return false;
}

// Task Form Submit
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('taskForm');
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();

            // Валидация матрицы Эйзенхауэра
            if (!validateEisenhower()) {
                return;
            }

            const taskId = document.getElementById('taskId').value;
            const tagIds = Array.from(document.querySelectorAll('.tag-checkbox:checked'))
                .map(cb => parseInt(cb.value));

            // Получаем значения матрицы Эйзенхауэра
            const importance = document.querySelector('input[name="eisenhower_importance"]:checked');
            const urgency = document.querySelector('input[name="eisenhower_urgency"]:checked');

            const data = {
                title: document.getElementById('title').value,
                ideichnaya_link: document.getElementById('ideichnaya_link').value || null,
                description: document.getElementById('description').value || null,
                assignee: document.getElementById('assignee').value || null,
                executor: document.getElementById('executor').value || null,
                priority: document.getElementById('priority').value,
                status: document.getElementById('status').value,
                rice_value: document.getElementById('rice_value').value ? parseInt(document.getElementById('rice_value').value) : null,
                rice_reach: document.getElementById('rice_reach').value ? parseInt(document.getElementById('rice_reach').value) : null,
                rice_confidence: document.getElementById('rice_confidence').value ? parseInt(document.getElementById('rice_confidence').value) : null,
                budget_impact: document.getElementById('budget_impact').value ? parseFloat(document.getElementById('budget_impact').value) : 1.0,
                eisenhower_urgent: urgency ? urgency.value === 'urgent' : null,
                eisenhower_important: importance ? importance.value === 'important' : null,
                tag_ids: tagIds
            };

            try {
                const url = taskId ? `/api/tasks/${taskId}` : '/api/tasks';
                const method = taskId ? 'PUT' : 'POST';

                const response = await fetch(url, {
                    method: method,
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                if (response.ok) {
                    // Закрываем модалку
                    closeModal();
                    // Также закрываем viewModal если был открыт
                    closeViewModal();
                    // Показываем уведомление
                    showNotification(taskId ? 'Обновлено!' : 'Задача создана!');
                    // Reload page content
                    if (typeof loadTasks === 'function') loadTasks();
                    if (typeof loadRiceTasks === 'function') loadRiceTasks();
                    if (typeof loadEisenhowerTasks === 'function') loadEisenhowerTasks();
                    if (typeof loadDashboard === 'function') loadDashboard();
                    if (typeof loadDoneTasks === 'function') loadDoneTasks();
                } else {
                    showNotification('Ошибка сохранения', 'error');
                }
            } catch (error) {
                console.error('Error saving task:', error);
            }
        });
    }
});

// View Task Modal
async function openViewModal(taskId) {
    currentTaskId = taskId;

    try {
        const response = await fetch(`/api/tasks/${taskId}`);
        const task = await response.json();

        // Загружаем пользователей если ещё не загружены
        if (cachedUsers.length === 0) {
            await loadUsers();
        }

        const modal = document.getElementById('viewTaskModal');
        document.getElementById('viewTaskTitle').textContent = task.title;

        const quadrantNames = {
            1: 'Сделать сейчас',
            2: 'Запланировать',
            3: 'Делегировать',
            4: 'Удалить/Отложить'
        };

        // Получаем emoji и цвет для пользователей
        const assigneeEmoji = getUserEmoji(task.assignee);
        const assigneeColor = getUserColor(task.assignee);
        const executorEmoji = getUserEmoji(task.executor);
        const executorColor = getUserColor(task.executor);

        const content = document.getElementById('viewTaskContent');
        content.innerHTML = `
            ${task.ideichnaya_link ? `
                <div class="detail-row">
                    <span class="detail-label">Ссылка:</span>
                    <span class="detail-value"><a href="${task.ideichnaya_link}" target="_blank">${task.ideichnaya_link}</a></span>
                </div>
            ` : ''}
            ${task.description ? `
                <div class="detail-row">
                    <span class="detail-label">Описание:</span>
                    <span class="detail-value">${task.description}</span>
                </div>
            ` : ''}
            <div class="detail-row">
                <span class="detail-label">Приоритет:</span>
                <span class="detail-value"><span class="priority-badge priority-${task.priority.toLowerCase()}">${task.priority}</span></span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Статус:</span>
                <span class="detail-value">
                    <select onchange="updateTaskStatus(${task.id}, this.value)" class="rice-select">
                        <option value="New" ${task.status === 'New' ? 'selected' : ''}>New</option>
                        <option value="Collecting" ${task.status === 'Collecting' ? 'selected' : ''}>Collecting</option>
                        <option value="Ready for Dev" ${task.status === 'Ready for Dev' ? 'selected' : ''}>Ready for Dev</option>
                        <option value="In Dev" ${task.status === 'In Dev' ? 'selected' : ''}>In Dev</option>
                        <option value="Ready for Release" ${task.status === 'Ready for Release' ? 'selected' : ''}>Ready for Release</option>
                        <option value="Done" ${task.status === 'Done' ? 'selected' : ''}>Done</option>
                    </select>
                </span>
            </div>
            ${task.assignee ? `
                <div class="detail-row">
                    <span class="detail-label">Постановщик:</span>
                    <span class="detail-value">
                        <div class="avatar-with-name">
                            <div class="avatar avatar-sm" style="background-color: ${assigneeColor}20; border: 2px solid ${assigneeColor}">
                                ${assigneeEmoji}
                            </div>
                            <span class="name">${task.assignee}</span>
                        </div>
                    </span>
                </div>
            ` : ''}
            ${task.executor ? `
                <div class="detail-row">
                    <span class="detail-label">Исполнитель:</span>
                    <span class="detail-value">
                        <div class="avatar-with-name">
                            <div class="avatar avatar-sm" style="background-color: ${executorColor}20; border: 2px solid ${executorColor}">
                                ${executorEmoji}
                            </div>
                            <span class="name">${task.executor}</span>
                        </div>
                    </span>
                </div>
            ` : ''}
            ${task.tags.length > 0 ? `
                <div class="detail-row">
                    <span class="detail-label">Теги:</span>
                    <span class="detail-value">${task.tags.map(t => `<span class="mini-tag" style="background-color: ${t.color}">${t.name}</span>`).join(' ')}</span>
                </div>
            ` : ''}
            ${task.rice_score ? `
                <div class="detail-row">
                    <span class="detail-label">Priority Score:</span>
                    <span class="detail-value"><strong>${task.rice_score.toFixed(2)}</strong> (V: ${task.rice_value}, R: ${task.rice_reach}, B: ${task.budget_impact || 1.0}, C: ${task.rice_confidence}%)</span>
                </div>
            ` : ''}
            <div class="detail-row">
                <span class="detail-label">Эйзенхауэр:</span>
                <span class="detail-value">${quadrantNames[task.eisenhower_quadrant]} (${task.eisenhower_urgent ? 'Срочно' : 'Не срочно'}, ${task.eisenhower_important ? 'Важно' : 'Не важно'})</span>
            </div>

            ${renderAttachments(task.attachments)}
        `;

        // Load comments
        loadComments(task.comments);

        if (modal.tagName === 'DIALOG') {
            modal.showModal();
        } else {
            modal.classList.add('active');
        }

        // Инициализируем dropzone для вложений после рендеринга
        setTimeout(() => initAttachmentDropzone(), 100);
    } catch (error) {
        console.error('Error loading task:', error);
    }
}

function closeViewModal() {
    const modal = document.getElementById('viewTaskModal');
    if (modal) {
        if (modal.tagName === 'DIALOG') {
            modal.close();
        } else {
            modal.classList.remove('active');
            modal.style.display = 'none';
            setTimeout(() => {
                modal.style.display = '';
            }, 100);
        }
    }
    currentTaskId = null;
}

async function updateTaskStatus(taskId, status) {
    try {
        await fetch(`/api/tasks/${taskId}/status`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status })
        });

        // Reload page content
        if (typeof loadTasks === 'function') loadTasks();
    } catch (error) {
        console.error('Error updating status:', error);
    }
}

function editCurrentTask() {
    const taskId = currentTaskId; // Сохраняем ID перед закрытием
    closeViewModal();
    openModal(taskId);
}

async function deleteCurrentTask() {
    if (!confirm('Вы уверены, что хотите удалить эту задачу?')) return;

    try {
        await fetch(`/api/tasks/${currentTaskId}`, { method: 'DELETE' });
        closeViewModal();

        // Reload page content
        if (typeof loadTasks === 'function') loadTasks();
        if (typeof loadRiceTasks === 'function') loadRiceTasks();
        if (typeof loadEisenhowerTasks === 'function') loadEisenhowerTasks();
        if (typeof loadDashboard === 'function') loadDashboard();
    } catch (error) {
        console.error('Error deleting task:', error);
    }
}

// Comments
function loadComments(comments) {
    const container = document.getElementById('commentsList');

    if (comments.length === 0) {
        container.innerHTML = '<p class="empty-message">Нет комментариев</p>';
        return;
    }

    container.innerHTML = comments.map(comment => `
        <div class="comment-item">
            <div class="comment-header">
                <span class="comment-author">${comment.author || 'Аноним'}</span>
                <span class="comment-date">${new Date(comment.created_at).toLocaleString('ru')}</span>
            </div>
            <p class="comment-text">${comment.text}</p>
        </div>
    `).join('');
}

document.addEventListener('DOMContentLoaded', function() {
    const commentForm = document.getElementById('commentForm');
    if (commentForm) {
        commentForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            const text = document.getElementById('commentText').value;
            const author = document.getElementById('commentAuthor').value;

            if (!text.trim()) return;

            try {
                const response = await fetch(`/api/tasks/${currentTaskId}/comments`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text, author: author || null })
                });

                if (response.ok) {
                    document.getElementById('commentText').value = '';
                    // Reload task to get updated comments
                    openViewModal(currentTaskId);
                }
            } catch (error) {
                console.error('Error adding comment:', error);
            }
        });
    }
});

// Tags Modal
function openTagsModal() {
    const modal = document.getElementById('tagsModal');
    loadTagsList();
    if (modal.tagName === 'DIALOG') {
        modal.showModal();
    } else {
        modal.classList.add('active');
    }
}

function closeTagsModal() {
    const modal = document.getElementById('tagsModal');
    if (modal.tagName === 'DIALOG') {
        modal.close();
    } else {
        modal.classList.remove('active');
    }
}

async function loadTagsList() {
    try {
        const response = await fetch('/api/tags');
        const tags = await response.json();

        const container = document.getElementById('tagsList');
        container.innerHTML = tags.map(tag => `
            <div class="tag-item">
                <div class="tag-info">
                    <span class="tag-emoji">${tag.emoji || '🏷️'}</span>
                    <span class="tag-color-preview" style="background-color: ${tag.color}"></span>
                    <span class="tag-name">${tag.name}</span>
                </div>
                <button class="icon-btn danger" onclick="deleteTag(${tag.id})" title="Удалить тег">
                    <span class="material-icons-round">close</span>
                </button>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading tags:', error);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const newTagForm = document.getElementById('newTagForm');
    if (newTagForm) {
        newTagForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            const name = document.getElementById('newTagName').value;
            const color = document.getElementById('newTagColor').value;
            const emoji = document.getElementById('newTagEmoji').value || '🏷️';

            try {
                const response = await fetch('/api/tags', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, color, emoji })
                });

                if (response.ok) {
                    document.getElementById('newTagName').value = '';
                    document.getElementById('newTagEmoji').value = '';
                    loadTagsList();
                    loadTags();
                    if (typeof loadTagsFilter === 'function') loadTagsFilter();
                } else {
                    const error = await response.json();
                    alert(error.error || 'Ошибка создания тега');
                }
            } catch (error) {
                console.error('Error creating tag:', error);
            }
        });
    }
});

async function deleteTag(tagId) {
    if (!confirm('Удалить этот тег?')) return;

    try {
        await fetch(`/api/tags/${tagId}`, { method: 'DELETE' });
        loadTagsList();
        loadTags();
        if (typeof loadTagsFilter === 'function') loadTagsFilter();
        if (typeof loadTasks === 'function') loadTasks();
    } catch (error) {
        console.error('Error deleting tag:', error);
    }
}

// Dropdown Menu
function toggleDropdown(button) {
    const dropdown = button.closest('.dropdown');
    const isActive = dropdown.classList.contains('active');

    // Закрываем все dropdown
    closeDropdowns();

    // Открываем текущий, если он был закрыт
    if (!isActive) {
        dropdown.classList.add('active');
    }
}

function closeDropdowns() {
    document.querySelectorAll('.dropdown.active').forEach(d => {
        d.classList.remove('active');
    });
}

// Закрываем dropdown при клике вне
document.addEventListener('click', function(e) {
    if (!e.target.closest('.dropdown')) {
        closeDropdowns();
    }
});

// Import Modal
function openImportModal() {
    const modal = document.getElementById('importModal');
    // Сбрасываем состояние
    document.getElementById('importProgress').style.display = 'none';
    document.getElementById('importResult').style.display = 'none';
    document.getElementById('importDropzone').style.display = 'block';
    document.querySelector('.import-info').style.display = 'block';
    if (modal.tagName === 'DIALOG') {
        modal.showModal();
    } else {
        modal.classList.add('active');
    }
}

function closeImportModal() {
    const modal = document.getElementById('importModal');
    if (modal.tagName === 'DIALOG') {
        modal.close();
    } else {
        modal.classList.remove('active');
    }
}

// Import file handling
document.addEventListener('DOMContentLoaded', function() {
    const dropzone = document.getElementById('importDropzone');
    const fileInput = document.getElementById('importFileInput');

    if (dropzone && fileInput) {
        // Click to select file
        dropzone.addEventListener('click', () => fileInput.click());

        // File selected
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleImportFile(e.target.files[0]);
            }
        });

        // Drag and drop
        dropzone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropzone.classList.add('dragover');
        });

        dropzone.addEventListener('dragleave', () => {
            dropzone.classList.remove('dragover');
        });

        dropzone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropzone.classList.remove('dragover');
            if (e.dataTransfer.files.length > 0) {
                handleImportFile(e.dataTransfer.files[0]);
            }
        });
    }
});

async function handleImportFile(file) {
    const validExtensions = ['.xlsx', '.xls', '.csv'];
    const fileName = file.name.toLowerCase();
    const isValid = validExtensions.some(ext => fileName.endsWith(ext));

    if (!isValid) {
        alert('Неподдерживаемый формат файла. Используйте .xlsx или .csv');
        return;
    }

    // Показываем прогресс
    document.getElementById('importDropzone').style.display = 'none';
    document.querySelector('.import-info').style.display = 'none';
    document.getElementById('importProgress').style.display = 'block';
    document.getElementById('importResult').style.display = 'none';

    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');

    progressFill.style.width = '30%';
    progressText.textContent = 'Загрузка файла...';

    const formData = new FormData();
    formData.append('file', file);

    try {
        progressFill.style.width = '60%';
        progressText.textContent = 'Обработка данных...';

        const response = await fetch('/api/import', {
            method: 'POST',
            body: formData
        });

        progressFill.style.width = '100%';

        const result = await response.json();

        // Скрываем прогресс, показываем результат
        document.getElementById('importProgress').style.display = 'none';
        const resultDiv = document.getElementById('importResult');
        resultDiv.style.display = 'block';

        if (response.ok && result.success) {
            resultDiv.className = 'import-result success';
            resultDiv.innerHTML = `
                <h4>
                    <span class="material-icons-round">check_circle</span>
                    Импорт завершён
                </h4>
                <div class="stats">
                    <div class="stat">
                        <span class="stat-num">${result.imported}</span>
                        <span class="stat-label">Импортировано</span>
                    </div>
                    <div class="stat">
                        <span class="stat-num">${result.total}</span>
                        <span class="stat-label">Всего строк</span>
                    </div>
                    <div class="stat">
                        <span class="stat-num">${result.errors_count}</span>
                        <span class="stat-label">Ошибок</span>
                    </div>
                </div>
                ${result.errors.length > 0 ? `
                    <div class="errors-list">
                        ${result.errors.map(err => `<p>${err}</p>`).join('')}
                    </div>
                ` : ''}
                <button class="btn btn-primary" onclick="closeImportModal(); if(typeof loadTasks === 'function') loadTasks();" style="margin-top: 16px;">
                    Готово
                </button>
            `;
        } else {
            resultDiv.className = 'import-result error';
            resultDiv.innerHTML = `
                <h4>
                    <span class="material-icons-round">error</span>
                    Ошибка импорта
                </h4>
                <p>${result.error || 'Неизвестная ошибка'}</p>
                <button class="btn btn-secondary" onclick="resetImportModal();" style="margin-top: 16px;">
                    Попробовать снова
                </button>
            `;
        }
    } catch (error) {
        console.error('Import error:', error);
        document.getElementById('importProgress').style.display = 'none';
        const resultDiv = document.getElementById('importResult');
        resultDiv.style.display = 'block';
        resultDiv.className = 'import-result error';
        resultDiv.innerHTML = `
            <h4>
                <span class="material-icons-round">error</span>
                Ошибка соединения
            </h4>
            <p>Не удалось загрузить файл. Проверьте соединение и попробуйте снова.</p>
            <button class="btn btn-secondary" onclick="resetImportModal();" style="margin-top: 16px;">
                Попробовать снова
            </button>
        `;
    }
}

function resetImportModal() {
    document.getElementById('importProgress').style.display = 'none';
    document.getElementById('importResult').style.display = 'none';
    document.getElementById('importDropzone').style.display = 'block';
    document.querySelector('.import-info').style.display = 'block';
    document.getElementById('importFileInput').value = '';
}

// Close modals on outside click
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('active');
    }
});

// Close modals on Escape
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        // Закрываем старые модалки
        document.querySelectorAll('.modal.active').forEach(modal => {
            if (modal.tagName !== 'DIALOG') {
                modal.classList.remove('active');
            }
            // DaisyUI dialog закрывается автоматически по ESC
        });
        closeDropdowns();
    }
});


// ======================= ATTACHMENTS (Вложения) =======================
let cachedUsers = [];

async function loadAttachments(taskId) {
    try {
        const response = await fetch(`/api/tasks/${taskId}/attachments`);
        return await response.json();
    } catch (error) {
        console.error('Error loading attachments:', error);
        return [];
    }
}

function renderAttachments(attachments) {
    if (!attachments || attachments.length === 0) {
        return '';
    }

    const attachmentsHtml = attachments.map(att => `
        <div class="attachment-item" data-id="${att.id}">
            <div class="attachment-icon">
                <span class="material-icons-round">${att.icon}</span>
            </div>
            <div class="attachment-info">
                <div class="attachment-name">${att.original_name}</div>
                <div class="attachment-size">${att.formatted_size}</div>
            </div>
            <div class="attachment-actions">
                <a href="/api/attachments/${att.id}/download" class="icon-btn" title="Скачать">
                    <span class="material-icons-round">download</span>
                </a>
                <button class="icon-btn danger" onclick="deleteAttachment(${att.id})" title="Удалить">
                    <span class="material-icons-round">delete</span>
                </button>
            </div>
        </div>
    `).join('');

    return `
        <div class="attachments-section">
            <h3>
                <span class="material-icons-round">attach_file</span>
                Вложения (${attachments.length})
            </h3>
            <div class="attachments-list">
                ${attachmentsHtml}
            </div>
            <div class="upload-dropzone" id="uploadDropzone" onclick="document.getElementById('attachmentFileInput').click()">
                <span class="material-icons-round">cloud_upload</span>
                <p>Перетащите файл или нажмите для загрузки</p>
                <span class="upload-formats">До 16 MB. Изображения, PDF, документы</span>
                <input type="file" id="attachmentFileInput" hidden>
            </div>
            <div class="upload-progress" id="uploadProgress">
                <div class="progress-bar">
                    <div class="progress-fill" id="uploadProgressFill"></div>
                </div>
                <div class="progress-text" id="uploadProgressText">Загрузка...</div>
            </div>
        </div>
    `;
}

async function deleteAttachment(attachmentId) {
    if (!confirm('Удалить это вложение?')) return;

    try {
        const response = await fetch(`/api/attachments/${attachmentId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            // Обновляем отображение задачи
            if (currentTaskId) {
                openViewModal(currentTaskId);
            }
            showNotification('Вложение удалено');
        }
    } catch (error) {
        console.error('Error deleting attachment:', error);
        showNotification('Ошибка удаления', 'error');
    }
}

async function uploadAttachment(file) {
    if (!currentTaskId) return;

    const maxSize = 16 * 1024 * 1024; // 16MB
    if (file.size > maxSize) {
        showNotification('Файл слишком большой (макс. 16MB)', 'error');
        return;
    }

    const progressDiv = document.getElementById('uploadProgress');
    const progressFill = document.getElementById('uploadProgressFill');
    const progressText = document.getElementById('uploadProgressText');

    if (progressDiv) {
        progressDiv.classList.add('active');
        progressFill.style.width = '0%';
        progressText.textContent = 'Загрузка...';
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const xhr = new XMLHttpRequest();

        xhr.upload.onprogress = function(e) {
            if (e.lengthComputable && progressFill) {
                const percent = (e.loaded / e.total) * 100;
                progressFill.style.width = percent + '%';
                progressText.textContent = `Загрузка: ${Math.round(percent)}%`;
            }
        };

        xhr.onload = function() {
            if (progressDiv) progressDiv.classList.remove('active');

            if (xhr.status === 201) {
                showNotification('Файл загружен');
                openViewModal(currentTaskId);
            } else {
                const error = JSON.parse(xhr.responseText);
                showNotification(error.error || 'Ошибка загрузки', 'error');
            }
        };

        xhr.onerror = function() {
            if (progressDiv) progressDiv.classList.remove('active');
            showNotification('Ошибка соединения', 'error');
        };

        xhr.open('POST', `/api/tasks/${currentTaskId}/attachments`);
        xhr.send(formData);

    } catch (error) {
        console.error('Error uploading attachment:', error);
        if (progressDiv) progressDiv.classList.remove('active');
        showNotification('Ошибка загрузки', 'error');
    }
}

// Инициализация drag-drop для вложений
function initAttachmentDropzone() {
    const dropzone = document.getElementById('uploadDropzone');
    const fileInput = document.getElementById('attachmentFileInput');

    if (!dropzone || !fileInput) return;

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            uploadAttachment(e.target.files[0]);
            e.target.value = '';
        }
    });

    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('drag-over');
    });

    dropzone.addEventListener('dragleave', () => {
        dropzone.classList.remove('drag-over');
    });

    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('drag-over');
        if (e.dataTransfer.files.length > 0) {
            uploadAttachment(e.dataTransfer.files[0]);
        }
    });
}


// ======================= USERS & AVATARS (Пользователи и аватары) =======================

async function loadUsers() {
    try {
        const response = await fetch('/api/users');
        cachedUsers = await response.json();
        return cachedUsers;
    } catch (error) {
        console.error('Error loading users:', error);
        return [];
    }
}

async function loadAvatars() {
    try {
        const response = await fetch('/api/avatars');
        return await response.json();
    } catch (error) {
        console.error('Error loading avatars:', error);
        return [];
    }
}

function getUserEmoji(userName) {
    const user = cachedUsers.find(u => u.name === userName);
    return user ? user.emoji : '👤';
}

function getUserColor(userName) {
    const user = cachedUsers.find(u => u.name === userName);
    return user ? user.color : '#14b8a6';
}

function renderUserWithAvatar(userName, size = '') {
    if (!userName) return '';

    const emoji = getUserEmoji(userName);
    const color = getUserColor(userName);
    const sizeClass = size ? `avatar-${size}` : '';

    return `
        <div class="avatar-with-name">
            <div class="avatar ${sizeClass}" style="background-color: ${color}20; border: 2px solid ${color}">
                ${emoji}
            </div>
            <span class="name">${userName}</span>
        </div>
    `;
}

// Автодополнение для полей пользователей
function initUserAutocomplete(inputId, containerId) {
    const input = document.getElementById(inputId);
    if (!input) return;

    let autocompleteDiv = document.getElementById(`${inputId}-autocomplete`);
    if (!autocompleteDiv) {
        autocompleteDiv = document.createElement('div');
        autocompleteDiv.id = `${inputId}-autocomplete`;
        autocompleteDiv.className = 'user-autocomplete';
        input.parentElement.style.position = 'relative';
        input.parentElement.appendChild(autocompleteDiv);
    }

    input.addEventListener('input', async function() {
        const value = this.value.toLowerCase().trim();

        if (value.length < 1) {
            autocompleteDiv.classList.remove('show');
            return;
        }

        if (cachedUsers.length === 0) {
            await loadUsers();
        }

        const matches = cachedUsers.filter(u =>
            u.name.toLowerCase().includes(value)
        ).slice(0, 5);

        if (matches.length === 0) {
            autocompleteDiv.classList.remove('show');
            return;
        }

        autocompleteDiv.innerHTML = matches.map(user => `
            <div class="user-autocomplete-item" onclick="selectUser('${inputId}', '${user.name}')">
                <div class="avatar" style="background-color: ${user.color}20; border: 2px solid ${user.color}">
                    ${user.emoji}
                </div>
                <span class="name">${user.name}</span>
            </div>
        `).join('');

        autocompleteDiv.classList.add('show');
    });

    input.addEventListener('blur', function() {
        // Небольшая задержка чтобы успеть кликнуть по элементу
        setTimeout(() => autocompleteDiv.classList.remove('show'), 200);
    });
}

function selectUser(inputId, userName) {
    const input = document.getElementById(inputId);
    if (input) {
        input.value = userName;
    }
    const autocomplete = document.getElementById(`${inputId}-autocomplete`);
    if (autocomplete) {
        autocomplete.classList.remove('show');
    }
}

// Инициализация автодополнения при загрузке
document.addEventListener('DOMContentLoaded', async function() {
    await loadUsers();
    initUserAutocomplete('assignee');
    initUserAutocomplete('executor');
});


// ======================= USERS MODAL (Модальное окно пользователей) =======================

let currentEditingUser = null;
let selectedAvatar = 'default';
let selectedColor = '#14b8a6';

function openUsersModal() {
    const modal = document.getElementById('usersModal');
    if (modal) {
        loadUsersList();
        loadAvatarSelector();
        if (modal.tagName === 'DIALOG') {
            modal.showModal();
        } else {
            modal.classList.add('active');
        }
    }
}

function closeUsersModal() {
    const modal = document.getElementById('usersModal');
    if (modal) {
        if (modal.tagName === 'DIALOG') {
            modal.close();
        } else {
            modal.classList.remove('active');
        }
    }
    resetUserForm();
}

function resetUserForm() {
    const nameInput = document.getElementById('newUserName');
    if (nameInput) nameInput.value = '';
    selectedAvatar = 'default';
    selectedColor = '#14b8a6';
    currentEditingUser = null;
    updateAvatarPreview();
}

async function loadUsersList() {
    await loadUsers();

    const container = document.getElementById('usersList');
    if (!container) return;

    if (cachedUsers.length === 0) {
        container.innerHTML = '<p class="empty-message">Нет пользователей</p>';
        return;
    }

    container.innerHTML = cachedUsers.map(user => `
        <div class="user-item" data-id="${user.id}">
            <div class="avatar" style="background-color: ${user.color}20; border: 2px solid ${user.color}">
                ${user.emoji}
            </div>
            <span class="user-name">${user.name}</span>
            <div class="user-actions">
                <button class="icon-btn" onclick="editUser(${user.id})" title="Редактировать">
                    <span class="material-icons-round">edit</span>
                </button>
                <button class="icon-btn danger" onclick="deleteUser(${user.id})" title="Удалить">
                    <span class="material-icons-round">delete</span>
                </button>
            </div>
        </div>
    `).join('');
}

async function loadAvatarSelector() {
    const avatars = await loadAvatars();
    const container = document.getElementById('avatarSelector');
    if (!container) return;

    container.innerHTML = avatars.map(avatar => `
        <div class="avatar-option ${avatar.id === selectedAvatar ? 'selected' : ''}"
             data-id="${avatar.id}"
             title="${avatar.name}"
             onclick="selectAvatar('${avatar.id}')">
            ${avatar.emoji}
        </div>
    `).join('');
}

function selectAvatar(avatarId) {
    selectedAvatar = avatarId;
    document.querySelectorAll('.avatar-option').forEach(opt => {
        opt.classList.toggle('selected', opt.dataset.id === avatarId);
    });
    updateAvatarPreview();
}

function selectColor(color) {
    selectedColor = color;
    document.querySelectorAll('.color-option').forEach(opt => {
        opt.classList.toggle('selected', opt.style.backgroundColor === color);
    });
    updateAvatarPreview();
}

function updateAvatarPreview() {
    const preview = document.getElementById('avatarPreview');
    if (preview) {
        const avatarEmoji = getAvatarEmoji(selectedAvatar);
        preview.innerHTML = avatarEmoji;
        preview.style.backgroundColor = selectedColor + '20';
        preview.style.border = `2px solid ${selectedColor}`;
    }
}

function getAvatarEmoji(avatarId) {
    const avatarMap = {
        'default': '👤', 'cat': '🐱', 'dog': '🐶', 'bear': '🐻', 'fox': '🦊',
        'owl': '🦉', 'penguin': '🐧', 'rabbit': '🐰', 'tiger': '🐯', 'wolf': '🐺',
        'unicorn': '🦄', 'dragon': '🐉', 'rocket': '🚀', 'star': '⭐', 'fire': '🔥'
    };
    return avatarMap[avatarId] || '👤';
}

async function saveUser() {
    const nameInput = document.getElementById('newUserName');
    const name = nameInput ? nameInput.value.trim() : '';

    if (!name) {
        showNotification('Введите имя пользователя', 'error');
        return;
    }

    const data = {
        name: name,
        avatar: selectedAvatar,
        color: selectedColor
    };

    try {
        let url = '/api/users';
        let method = 'POST';

        if (currentEditingUser) {
            url = `/api/users/${currentEditingUser}`;
            method = 'PUT';
        }

        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            showNotification(currentEditingUser ? 'Пользователь обновлён' : 'Пользователь создан');
            resetUserForm();
            loadUsersList();
            await loadUsers(); // Обновляем кэш
        } else {
            const error = await response.json();
            showNotification(error.error || 'Ошибка', 'error');
        }
    } catch (error) {
        console.error('Error saving user:', error);
        showNotification('Ошибка сохранения', 'error');
    }
}

async function editUser(userId) {
    const user = cachedUsers.find(u => u.id === userId);
    if (!user) return;

    currentEditingUser = userId;
    selectedAvatar = user.avatar;
    selectedColor = user.color;

    const nameInput = document.getElementById('newUserName');
    if (nameInput) nameInput.value = user.name;

    loadAvatarSelector();
    updateAvatarPreview();
}

async function deleteUser(userId) {
    if (!confirm('Удалить этого пользователя?')) return;

    try {
        const response = await fetch(`/api/users/${userId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            showNotification('Пользователь удалён');
            loadUsersList();
            await loadUsers(); // Обновляем кэш
        }
    } catch (error) {
        console.error('Error deleting user:', error);
        showNotification('Ошибка удаления', 'error');
    }
}

function toggleAvatarSelector() {
    const container = document.getElementById('avatarSelectorContainer');
    if (container) {
        container.style.display = container.style.display === 'none' ? 'block' : 'none';
        if (container.style.display === 'block') {
            loadAvatarSelector();
        }
    }
}

