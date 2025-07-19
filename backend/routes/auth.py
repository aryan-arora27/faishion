from flask import Blueprint, request, jsonify
from database import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    skin_color = data.get('skin_color', None) 

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    new_user = User(username=username, password=password, skin_color=skin_color)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'message': 'User registered successfully',
        'user_id': new_user.id,
        'skin_color': new_user.skin_color
    }), 200

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username, password=password).first()
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    return jsonify({
        'message': 'Login successful',
        'user_id': user.id,
        'skin_color': user.skin_color
    }), 200

@auth_bp.route('/set_skin_color', methods=['POST'])
def set_skin_color():
    data = request.get_json()
    user_id = data['user_id']
    skin_color = data['skin_color']

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.skin_color = skin_color
    db.session.commit()

    return jsonify({"message": "Skin color updated successfully"}), 200
