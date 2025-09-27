from flask import Blueprint, redirect, request, make_response, url_for, render_template, abort, flash
from models.user import usuarios

login_bp = Blueprint('login', __name__, template_folder='templates')

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.cookies.get('usuario'):
        return redirect(url_for('index'))
    mensagem = "Faça login para acessar nossos serviços"
    if request.method == 'POST':
        email = request.form['email'].lower()
        senha = request.form['senha']
        if email in usuarios.emails:
            usuario = usuarios.lista[usuarios.emails[email]]
            if usuario.email == email and usuario.senha == senha:
                resposta = make_response(redirect(url_for('index')))
                resposta.set_cookie('usuario', usuario.nome, max_age=60*30)
                return resposta
        mensagem = "Usuário ou senha inválido"
    flash(mensagem)
    return render_template('auth/login.html')
    
@login_bp.route('/logout', methods=['GET'])
def logout():
    resposta = make_response(redirect(url_for('login.login')))
    resposta.set_cookie('usuario', '', expires=0)
    return resposta