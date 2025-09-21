from flask import Blueprint, redirect, request, make_response, url_for, render_template, abort, flash
from models.user import usuarios

login_bp = Blueprint('login', __name__, template_folder='templates')

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    mensagem = "Faça login para acessar nossos serviços"
    if request.method == 'POST':
        email = request.form['email'].lower()
        senha = request.form['senha']
        if usuarios.lista.get(email):
            usuario = usuarios.lista[email]
            if usuario.senha == senha:
                resposta = make_response(redirect(url_for('index')))
                resposta.set_cookie('usuario', usuario.nome, max_age=60*30)
                return resposta
            mensagem = "Usuário ou senha inválidos"
        else:
            mensagem = "Usuário não existe"
    flash(mensagem)
    return render_template('auth/login.html')
    
@login_bp.route('/logout', methods=['GET'])
def logout():
    resposta = make_response(redirect(url_for('login.login')))
    resposta.set_cookie('usuario', '', expires=0)
    return resposta