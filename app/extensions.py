from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from faker import Faker
from flask_mail import Mail
from apscheduler.schedulers.background import BackgroundScheduler

login_manager = LoginManager()
login_manager.login_view = 'app.blueprints.auth.login'
db = SQLAlchemy()
bcrypt = Bcrypt()
security = Security()
mail = Mail()
faker = Faker(locale='pt_BR')
scheduler = BackgroundScheduler()