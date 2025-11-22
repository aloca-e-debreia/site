from flask import render_template, request, jsonify
from flask_security import roles_accepted
from flask_login import login_required, current_user
from app.blueprints.main import main_bp
from app.models import User, select_users_with_role, Rental, RentalStatus
from app import db, user_datastore, login_manager

@main_bp.route('/dashboard/rents')
def rents():
    rents = Rental.query.all()
    return render_template('main/rents.html', rents=rents)