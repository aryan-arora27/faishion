from flask import Blueprint, jsonify
from database import db, User 

debug_bp = Blueprint('debug', __name__)

@debug_bp.route('/debug/clear_db', methods=['POST'])
def clear_database():
    try:
        num_deleted = User.query.delete()
        db.session.commit()
        return {"message": f"Deleted {num_deleted} user(s)"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

@debug_bp.route('/debug/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([
        {
            "id": user.id,
            "username": user.username,
            "skin_color": user.skin_color
        } for user in users
    ])
