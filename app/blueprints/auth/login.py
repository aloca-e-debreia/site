from flask import redirect, request, url_for, render_template, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.blueprints.auth import auth_bp
from app.models import User
from app import bcrypt
from urllib.parse import urlparse, urljoin

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return (
        test_url.scheme in ('http', 'https') and
        ref_url.netloc == test_url.netloc
    )


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))           
    
    message = "Faça login para acessar nossos serviços"
    
    if request.method == 'POST':
        email = request.form['email'].lower()
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=False)
            
            next_page = request.form['next'] or request.args.get("next")

            if not next_page or not is_safe_url(next_page):
                return redirect(url_for('main.index'))
            
            return redirect(next_page)
        
        message = "Usuário ou senha inválido(s)"
    
    flash(message)
    next_page = request.args.get("next")
    return render_template('auth/login.html', next=next_page)
    
@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))