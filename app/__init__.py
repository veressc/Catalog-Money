from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os



db = SQLAlchemy()

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def create_app():
    app = Flask(__name__)

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # ✅ теперь 'app' уже есть

    # Настройки базы данных
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalog.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.routes import bp as main_routes
    app.register_blueprint(main_routes)

    return app

app = Flask(__name__, static_folder='static')
