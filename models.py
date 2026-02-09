from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

db = SQLAlchemy()

# Доступные аватары (эмодзи-иконки)
AVATAR_OPTIONS = [
    {'id': 'default', 'emoji': '👤', 'name': 'По умолчанию'},
    {'id': 'cat', 'emoji': '🐱', 'name': 'Кот'},
    {'id': 'dog', 'emoji': '🐶', 'name': 'Собака'},
    {'id': 'bear', 'emoji': '🐻', 'name': 'Медведь'},
    {'id': 'fox', 'emoji': '🦊', 'name': 'Лиса'},
    {'id': 'owl', 'emoji': '🦉', 'name': 'Сова'},
    {'id': 'penguin', 'emoji': '🐧', 'name': 'Пингвин'},
    {'id': 'rabbit', 'emoji': '🐰', 'name': 'Кролик'},
    {'id': 'tiger', 'emoji': '🐯', 'name': 'Тигр'},
    {'id': 'wolf', 'emoji': '🐺', 'name': 'Волк'},
    {'id': 'unicorn', 'emoji': '🦄', 'name': 'Единорог'},
    {'id': 'dragon', 'emoji': '🐉', 'name': 'Дракон'},
    {'id': 'rocket', 'emoji': '🚀', 'name': 'Ракета'},
    {'id': 'star', 'emoji': '⭐', 'name': 'Звезда'},
    {'id': 'fire', 'emoji': '🔥', 'name': 'Огонь'},
]


class User(db.Model):
    """Модель пользователя с аватаром"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    avatar = db.Column(db.String(50), nullable=False, default='default')
    color = db.Column(db.String(7), nullable=False, default='#14b8a6')  # HEX color
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_emoji(self):
        for avatar in AVATAR_OPTIONS:
            if avatar['id'] == self.avatar:
                return avatar['emoji']
        return '👤'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'avatar': self.avatar,
            'emoji': self.get_emoji(),
            'color': self.color,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    color = db.Column(db.String(7), nullable=False, default='#6366f1')  # HEX color
    emoji = db.Column(db.String(10), nullable=True, default='🏷️')  # Emoji для тега
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'emoji': self.emoji or '🏷️'
        }


class Group(db.Model):
    """Модель группы для организации задач"""
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)
    color = db.Column(db.String(7), nullable=False, default='#6366f1')
    icon = db.Column(db.String(10), nullable=True, default='📁')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'color': self.color,
            'icon': self.icon or '📁',
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# Связующая таблица для тегов задач
task_tags = db.Table('task_tags',
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    ideichnaya_link = db.Column(db.String(500), nullable=True)
    description = db.Column(db.Text, nullable=True)
    assignee = db.Column(db.String(100), nullable=True)  # Постановщик
    executor = db.Column(db.String(100), nullable=True)  # Исполнитель
    priority = db.Column(db.String(20), nullable=False, default='Medium')  # Low, Medium, High, Highest
    status = db.Column(db.String(30), nullable=False, default='New')  # New, Collecting, Ready for Dev, In Dev, Ready for Release, Done

    # Priority Score (формула: Score = (Value × Reach × Budget Impact) × Confidence)
    rice_value = db.Column(db.Integer, nullable=True)      # 1-5 (польза)
    rice_reach = db.Column(db.Integer, nullable=True)      # 1-5 (охват)
    rice_confidence = db.Column(db.Integer, nullable=True) # 0-100 (уверенность в %)
    budget_impact = db.Column(db.Float, nullable=True, default=1.0)  # 0.7, 1.0, 1.3, 1.6, 2.0 (влияние на бюджет)
    rice_score = db.Column(db.Float, nullable=True)        # автоматически вычисляется

    # Матрица Эйзенхауэра
    eisenhower_urgent = db.Column(db.Boolean, default=False)
    eisenhower_important = db.Column(db.Boolean, default=False)

    # Группа задачи
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Связи
    tags = db.relationship('Tag', secondary=task_tags, lazy='subquery',
                          backref=db.backref('tasks', lazy=True))
    group = db.relationship('Group', backref='tasks', lazy=True)

    # Связь с комментариями
    comments = db.relationship('Comment', backref='task', lazy=True, cascade='all, delete-orphan')

    def calculate_rice_score(self):
        """Рассчитать Priority Score = (Value × Reach × Budget Impact) × Confidence"""
        if all([self.rice_value is not None, self.rice_reach is not None, self.rice_confidence is not None]):
            budget = self.budget_impact if self.budget_impact is not None else 1.0
            # Формула: (Value × Reach × Budget Impact) × (Confidence / 100)
            self.rice_score = round((self.rice_value * self.rice_reach * budget) * (self.rice_confidence / 100.0), 2)
        else:
            self.rice_score = None

    def get_eisenhower_quadrant(self):
        if self.eisenhower_urgent and self.eisenhower_important:
            return 1  # Сделать сейчас
        elif not self.eisenhower_urgent and self.eisenhower_important:
            return 2  # Запланировать
        elif self.eisenhower_urgent and not self.eisenhower_important:
            return 3  # Делегировать
        else:
            return 4  # Удалить/Отложить

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'ideichnaya_link': self.ideichnaya_link,
            'description': self.description,
            'assignee': self.assignee,
            'executor': self.executor,
            'priority': self.priority,
            'status': self.status,
            'rice_value': self.rice_value,
            'rice_reach': self.rice_reach,
            'rice_confidence': self.rice_confidence,
            'budget_impact': self.budget_impact,
            'rice_score': self.rice_score,
            'eisenhower_urgent': self.eisenhower_urgent,
            'eisenhower_important': self.eisenhower_important,
            'eisenhower_quadrant': self.get_eisenhower_quadrant(),
            'tags': [tag.to_dict() for tag in self.tags],
            'group_id': self.group_id,
            'group': self.group.to_dict() if self.group else None,
            'comments': [comment.to_dict() for comment in self.comments],
            'attachments': [att.to_dict() for att in self.attachments],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'text': self.text,
            'author': self.author,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Attachment(db.Model):
    """Модель вложений для задач"""
    __tablename__ = 'attachments'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)  # Сохранённое имя файла (UUID)
    original_name = db.Column(db.String(255), nullable=False)  # Оригинальное имя файла
    file_size = db.Column(db.Integer, nullable=True)  # Размер в байтах
    mime_type = db.Column(db.String(100), nullable=True)  # MIME тип файла
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Связь с задачей
    task = db.relationship('Task', backref=db.backref('attachments', lazy=True, cascade='all, delete-orphan'))

    def get_file_icon(self):
        """Возвращает иконку Material Icons в зависимости от типа файла"""
        if not self.mime_type:
            return 'attach_file'

        if self.mime_type.startswith('image/'):
            return 'image'
        elif self.mime_type.startswith('video/'):
            return 'videocam'
        elif self.mime_type.startswith('audio/'):
            return 'audiotrack'
        elif 'pdf' in self.mime_type:
            return 'picture_as_pdf'
        elif 'word' in self.mime_type or 'document' in self.mime_type:
            return 'description'
        elif 'excel' in self.mime_type or 'spreadsheet' in self.mime_type:
            return 'table_chart'
        elif 'text' in self.mime_type:
            return 'article'
        elif 'zip' in self.mime_type or 'archive' in self.mime_type or 'rar' in self.mime_type:
            return 'folder_zip'
        else:
            return 'attach_file'

    def format_size(self):
        """Форматирует размер файла в человекочитаемый вид"""
        if not self.file_size:
            return '—'

        for unit in ['B', 'KB', 'MB', 'GB']:
            if self.file_size < 1024.0:
                return f"{self.file_size:.1f} {unit}"
            self.file_size /= 1024.0
        return f"{self.file_size:.1f} TB"

    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'filename': self.filename,
            'original_name': self.original_name,
            'file_size': self.file_size,
            'formatted_size': self.format_size(),
            'mime_type': self.mime_type,
            'icon': self.get_file_icon(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class RiceIdea(db.Model):
    """Модель для Priority Score-идей (задачи созданные только через раздел Priority Score)"""
    __tablename__ = 'rice_ideas'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Priority Score метрики (формула: Score = (Value × Reach × Budget Impact) × Confidence)
    value = db.Column(db.Integer, nullable=True)      # 1-5 (польза)
    reach = db.Column(db.Integer, nullable=True)      # 1-5 (охват)
    confidence = db.Column(db.Integer, nullable=True) # 0-100 (уверенность в %)
    budget_impact = db.Column(db.Float, nullable=True, default=1.0)  # 0.7, 1.0, 1.3, 1.6, 2.0
    rice_score = db.Column(db.Float, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def calculate_rice_score(self):
        """Рассчитать Priority Score = (Value × Reach × Budget Impact) × Confidence"""
        if all([self.value is not None, self.reach is not None, self.confidence is not None]):
            budget = self.budget_impact if self.budget_impact is not None else 1.0
            # Формула: (Value × Reach × Budget Impact) × (Confidence / 100)
            self.rice_score = round((self.value * self.reach * budget) * (self.confidence / 100.0), 2)
        else:
            self.rice_score = None
        return self.rice_score

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'value': self.value,
            'reach': self.reach,
            'confidence': self.confidence,
            'budget_impact': self.budget_impact,
            'rice_score': self.rice_score,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

