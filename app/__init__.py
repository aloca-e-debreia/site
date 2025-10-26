from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_bcrypt import Bcrypt

login_manager = LoginManager()
login_manager.login_view = 'app.blueprints.auth.login'
db = SQLAlchemy()
bcrypt = Bcrypt()
security = Security()
user_datastore = None

def get_user_datastore():
    return user_datastore

def create_roles():
    global user_datastore
    user_datastore.find_or_create_role(name='manager', descricao='Gerente do sistema')
    user_datastore.find_or_create_role(name='worker', descricao='Funcionário do sistema')
    user_datastore.find_or_create_role(name='client', descricao='Cliente do sistema')

def create_app():
    global user_datastore

    app = Flask(__name__)

    app.config['SECRET_KEY'] = "f53f95be4bd2b7e3b45ef48c5c78614a538a99539406b2efee72b174b8d47bde"
    app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
    app.config['SECURITY_PASSWORD_SALT'] = '5f3a2e9a76b8bde4a122cd3e671f81c2'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.config['SECURITY_BLUEPRINT_NAME'] = 'auth'
    app.config['SECURITY_VIEWS'] = False
    app.config['SECURITY_LOGIN_URL'] = '/auth/login'

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from app.models.user import Usuario, Role
    user_datastore = SQLAlchemyUserDatastore(db, Usuario, Role)
    security.init_app(app, user_datastore, register_blueprint=False)

    from app.blueprints.auth import auth_bp
    from app.blueprints.main.routes import main_bp
    from app.blueprints.main.errors import registrar_erros

    registrar_erros(app)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)

    return app