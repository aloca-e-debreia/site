from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():

    app = Flask(__name__)
    app.secret_key = "f53f95be4bd2b7e3b45ef48c5c78614a538a99539406b2efee72b174b8d47bde"

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from app.blueprints.auth.cadastro import auth_bp
    from app.blueprints.main.routes import main_bp
    from app.blueprints.main.errors import registrar_erros

    registrar_erros(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app