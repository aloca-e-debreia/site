from flask import Blueprint, request, redirect, url_for, render_template, make_response
from models.user import Usuario, usuarios

cadastro_bp = Blueprint('cadastro', __name__, template_folder='templates')

@cadastro_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    global next_id
    if request.method == 'POST':
        nome = request.form['nome'].lower().capitalize()
        sobrenome = request.form['sobrenome'].lower().capitalize()
        idade = int(request.form['idade'])
        cpf = request.form['CPF']
        email = request.form['email'].lower()
        senha = request.form['senha']

        usuario = Usuario(usuarios.next_id, nome, sobrenome, cpf, idade, email, senha)

        if not (usuarios.next_id, usuario) in usuarios.lista.items():
            usuarios.criar(usuario)
        resposta = make_response(redirect(url_for('index')))
        resposta.set_cookie('usuario', usuario.nome, max_age=60*30)
        return resposta
    
    return render_template('auth/cadastro.html')