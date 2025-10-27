from flask import redirect, request, url_for, render_template, flash
from flask_login import login_user, logout_user, login_required
from app.blueprints.auth import auth_bp
from app.models.user import User
from app import bcrypt

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.cookies.get('user'):
        return redirect(url_for('main.index'))           
    
    message = "Faça login para acessar nossos serviços"
    
    if request.method == 'POST':
        email = request.form['email'].lower()
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=False)
            return redirect(url_for('main.index'))
        
        message = "Usuário ou senha inválido(s)"
    
    flash(message)
    return render_template('auth/login.html')
    
@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))