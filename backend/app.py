from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from database import db  
from routes.debug import debug_bp

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fashion.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db.init_app(app)

from routes.auth import auth_bp
from routes.recommend import recommend_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(recommend_bp, url_prefix='/recommend')
app.register_blueprint(debug_bp)

if __name__ == '__main__':
    with app.app_context():
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        db.create_all()
    app.run(debug=True)
