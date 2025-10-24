from flask import redirect, request, url_for, render_template, abort, flash
from flask_login import login_user, logout_user, login_required
from app.blueprints.auth import auth_bp
from app.models.user import Usuario
from app import bcrypt

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.cookies.get('usuario'):
        return redirect(url_for('main.index'))
    
    mensagem = "Faça login para acessar nossos serviços"
    
    if request.method == 'POST':
        email = request.form['email'].lower()
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, senha):
            login_user(usuario, remember=False)
            return redirect(url_for('main.index'))
        
        mensagem = "Usuário ou senha inválido(s)"
    
    flash(mensagem)
    return render_template('auth/login.html')
    
@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))