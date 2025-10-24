from flask import render_template, redirect, url_for, abort
from flask_login import login_required, current_user
from flask_security import roles_accepted
from app.blueprints.main import main_bp
from app.models.user import Usuario
from app import login_manager

@login_manager.user_loader
def load_user(usuario_id):
    return Usuario.query.get(int(usuario_id))

@main_bp.route('/')
def index():
    return render_template('main/index.html', current_user=current_user)

@main_bp.route('/gerente')
@login_required
@roles_accepted('gerente')
def painel_admin():
    return 'Teste'