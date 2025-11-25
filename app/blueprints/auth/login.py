from flask import redirect, request, url_for, render_template, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.blueprints.auth import auth_bp
from app.models import User
from app import bcrypt, db, is_safe_url
import hashlib

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))           
    
    message = "Faça login para acessar nossos serviços"
    
    if request.method == 'POST':
        email = request.form['email'].lower()
        hashed_email = hashlib.sha256(email.encode()).hexdigest()
        password = request.form['password']

        user = User.query.filter_by(email_hash=hashed_email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=False)
            
            next_page = request.form['next'] or request.args.get("next")

            if not next_page or not is_safe_url(next_page):
                return redirect(url_for('main.index'))
            return redirect(next_page)
        
        message = "Usuário ou senha inválido(s)"
    
    flash(message)
    return render_template('auth/login.html')
    
@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth_bp.route('/api/account/remove', methods=['POST'])
@login_required
def remove_account():
    if request.method == "POST" and request.is_json:
        try:
            User.query.filter_by(id=current_user.id).delete()
            db.session.commit()
            return jsonify({
                "success" : True,
                "title" : "Conta removida com sucesso!",
                "icon" : "success",
                "redirect_url" : url_for('main.index')
            })
        except Exception as e:
            print("Erro:", e)
            return jsonify({
                "success" : False,
                "icon" : "error",
                "title" : "Erro.. Não foi possível localizar sua conta"
            })