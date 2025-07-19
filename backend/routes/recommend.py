import os
from flask import Blueprint, request, jsonify
from PIL import Image
import uuid
import json

from flask import current_app
from database import db, User, History

from database import User, History
from models import apparel_detector, color_extractor
from models.recommender_model import DualOutfitRecommender

recommend_bp = Blueprint('recommend', __name__)
model = DualOutfitRecommender.load_model("data/recommender_dual.pkl")

@recommend_bp.route('/upload', methods=['POST'])
def upload_and_recommend():
    user_id = request.form.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Invalid user'}), 400

    image = request.files.get('image')
    if not image:
        return jsonify({'error': 'No image provided'}), 400

    # Save image
    filename = f"{uuid.uuid4().hex}.jpg"
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    image.save(filepath)

    pil_img = Image.open(filepath)

    # Detection
    apparel_type, cropped_image = apparel_detector.detect(filepath)
    top_colors = color_extractor.extract_top_colors(cropped_image, top_or_bottom='top')

    # Recommend
    suggestions = model.recommend(top_type=apparel_type, top_colors=top_colors, skin_color=user.skin_color)

    # Save to DB
    history = History(
        user_id=user.id,
        image_path=filepath,
        apparel_type=apparel_type,
        color1=top_colors[0],
        color2=top_colors[1] if len(top_colors) > 1 else top_colors[0],
        suggestions=json.dumps(suggestions)
    )
    db.session.add(history)
    db.session.commit()

    return jsonify({
        'apparel': apparel_type,
        'colors': top_colors,
        'suggestions': suggestions,
        'image_url': f"/{filepath}"
    }), 200

@recommend_bp.route('/history/<user_id>', methods=['GET'])
def history(user_id):
    entries = History.query.filter_by(user_id=user_id).order_by(History.created_at.desc()).all()
    result = []
    for entry in entries:
        result.append({
            'date': entry.created_at.strftime('%Y-%m-%d %H:%M'),
            'image_url': f"/{entry.image_path}",
            'apparel': entry.apparel_type,
            'colors': [entry.color1, entry.color2],
            'suggestions': json.loads(entry.suggestions)
        })
    return jsonify(result), 200
