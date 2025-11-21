from app.extensions import *

user_datastore = None

def get_user_datastore():
    return user_datastore

def create_roles():
    global user_datastore
    user_datastore.find_or_create_role(name='manager', description='Gerente do sistema')
    user_datastore.find_or_create_role(name='worker', description='Funcionário do sistema')
    user_datastore.find_or_create_role(name='client', description='Cliente do sistema')
    db.session.commit()

def create_app():
    from flask import Flask
    from flask_security import SQLAlchemyUserDatastore

    global user_datastore

    app = Flask(__name__)

    app.config.from_pyfile('config.py')

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from app.models import User, Role
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore, register_blueprint=False)

    from app.blueprints.auth import auth_bp
    from app.blueprints.main.rental import main_bp
    from app.blueprints.main.errors import register_errors

    register_errors(app)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)

    from app.seeds import seed_init
    seed_init(app)

    return app