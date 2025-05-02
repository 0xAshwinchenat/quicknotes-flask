from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

app = None

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')  # << optional if folders are outside 'app'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quicknotes.db'
    app.config['SECRET_KEY'] = 'your-secret-key'

    db.init_app(app)

    CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

    from .routes import main
    app.register_blueprint(main)

    return app
