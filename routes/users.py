from flask import Blueprint, request, jsonify
from models import db, User, AVATAR_OPTIONS

users_bp = Blueprint('users', __name__)


@users_bp.route('/api/users', methods=['GET'])
def get_users():
    """Получить всех пользователей"""
    users = User.query.order_by(User.name).all()
    return jsonify([user.to_dict() for user in users])


@users_bp.route('/api/users', methods=['POST'])
def create_user():
    """Создать нового пользователя"""
    data = request.json

    # Проверяем, существует ли пользователь с таким именем
    existing = User.query.filter_by(name=data.get('name')).first()
    if existing:
        return jsonify({'error': 'Пользователь с таким именем уже существует'}), 400

    user = User(
        name=data.get('name'),
        avatar=data.get('avatar', 'default'),
        color=data.get('color', '#14b8a6')
    )

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201


@users_bp.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Получить пользователя по ID"""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


@users_bp.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Обновить пользователя"""
    user = User.query.get_or_404(user_id)
    data = request.json

    # Проверяем уникальность имени при изменении
    if 'name' in data and data['name'] != user.name:
        existing = User.query.filter_by(name=data['name']).first()
        if existing:
            return jsonify({'error': 'Пользователь с таким именем уже существует'}), 400

    user.name = data.get('name', user.name)
    user.avatar = data.get('avatar', user.avatar)
    user.color = data.get('color', user.color)

    db.session.commit()

    return jsonify(user.to_dict())


@users_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Удалить пользователя"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200


@users_bp.route('/api/users/by-name/<name>', methods=['GET'])
def get_user_by_name(name):
    """Получить пользователя по имени"""
    user = User.query.filter_by(name=name).first()
    if user:
        return jsonify(user.to_dict())
    return jsonify(None)


@users_bp.route('/api/users/find-or-create', methods=['POST'])
def find_or_create_user():
    """Найти пользователя по имени или создать нового"""
    data = request.json
    name = data.get('name', '').strip()

    if not name:
        return jsonify({'error': 'Имя обязательно'}), 400

    user = User.query.filter_by(name=name).first()

    if not user:
        user = User(
            name=name,
            avatar=data.get('avatar', 'default'),
            color=data.get('color', '#14b8a6')
        )
        db.session.add(user)
        db.session.commit()

    return jsonify(user.to_dict())


@users_bp.route('/api/avatars', methods=['GET'])
def get_avatars():
    """Получить список доступных аватаров"""
    return jsonify(AVATAR_OPTIONS)
