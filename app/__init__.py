from app.extensions import *

user_datastore = None

def is_safe_url(target):
    from urllib.parse import urlparse, urljoin
    from flask import request
    
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

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
    from app.blueprints.main.mailtest import register_app_email

    global user_datastore

    app = Flask(__name__)

    @app.template_filter()
    def currency(value, currency="BRL"):
        from babel.numbers import format_currency
        return format_currency(value, currency, locale="pt_BR")

    app.config.from_pyfile('config.py')

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    from app.models import User, Role, Rental, RentalStatus
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore, register_blueprint=False)

    @scheduler.scheduled_job('interval', days=1)
    def check_late_rentals():
        from datetime import datetime
        now = datetime.now()
        late_rentals = Rental.query.filter(
            Rental.status == RentalStatus.ACTIVE,
            Rental.dropoff.date < now
        ).all()

        for late_rental in late_rentals: late_rental.status = RentalStatus.LATE

        db.session.commit()

    from app.blueprints.auth import auth_bp
    from app.blueprints.main.rental import main_bp
    from app.blueprints.main.errors import register_errors

    register_errors(app)
    register_app_email(app)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp, url_prefix='/')

    from app.seeds import seed_init
    seed_init(app)

    return app