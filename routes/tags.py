from flask import Blueprint, request, jsonify
from models import db, Tag

tags_bp = Blueprint('tags', __name__)

# Предустановленные цвета для тегов (Material Design)
TAG_COLORS = [
    '#f44336',  # Red
    '#e91e63',  # Pink
    '#9c27b0',  # Purple
    '#673ab7',  # Deep Purple
    '#3f51b5',  # Indigo
    '#2196f3',  # Blue
    '#03a9f4',  # Light Blue
    '#00bcd4',  # Cyan
    '#009688',  # Teal
    '#4caf50',  # Green
    '#8bc34a',  # Light Green
    '#cddc39',  # Lime
    '#ffeb3b',  # Yellow
    '#ffc107',  # Amber
    '#ff9800',  # Orange
    '#ff5722',  # Deep Orange
    '#795548',  # Brown
    '#9e9e9e',  # Grey
    '#607d8b',  # Blue Grey
    '#000000',  # Black
]


@tags_bp.route('/api/tags', methods=['GET'])
def get_tags():
    """Получить все теги"""
    tags = Tag.query.order_by(Tag.name).all()
    return jsonify([tag.to_dict() for tag in tags])


@tags_bp.route('/api/tags', methods=['POST'])
def create_tag():
    """Создать новый тег"""
    data = request.json

    # Проверяем уникальность имени
    existing = Tag.query.filter(Tag.name.ilike(data.get('name'))).first()
    if existing:
        return jsonify({'error': 'Tag with this name already exists'}), 400

    tag = Tag(
        name=data.get('name'),
        color=data.get('color', '#6366f1'),
        emoji=data.get('emoji', '🏷️')
    )

    db.session.add(tag)
    db.session.commit()

    return jsonify(tag.to_dict()), 201


@tags_bp.route('/api/tags/<int:tag_id>', methods=['PUT'])
def update_tag(tag_id):
    """Обновить тег"""
    tag = Tag.query.get_or_404(tag_id)
    data = request.json

    tag.name = data.get('name', tag.name)
    tag.color = data.get('color', tag.color)
    tag.emoji = data.get('emoji', tag.emoji)

    db.session.commit()

    return jsonify(tag.to_dict())


@tags_bp.route('/api/tags/<int:tag_id>', methods=['DELETE'])
def delete_tag(tag_id):
    """Удалить тег"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return jsonify({'message': 'Tag deleted'}), 200


@tags_bp.route('/api/tag-colors', methods=['GET'])
def get_tag_colors():
    """Получить список доступных цветов для тегов"""
    return jsonify(TAG_COLORS)
