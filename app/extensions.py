from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_bcrypt import Bcrypt
from faker import Faker

login_manager = LoginManager()
login_manager.login_view = 'app.blueprints.auth.login'
db = SQLAlchemy()
bcrypt = Bcrypt()
security = Security()
faker = Faker(locale='pt_BR')