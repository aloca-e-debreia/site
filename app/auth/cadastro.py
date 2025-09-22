from flask import Blueprint, request, redirect, url_for, render_template
from models.user import Usuario, usuarios

cadastro_bp = Blueprint('cadastro', __name__, template_folder='templates')

@cadastro_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome'].lower().capitalize()
        sobrenome = request.form['sobrenome'].lower().capitalize()
        idade = int(request.form['idade'])
        cpf = request.form['CPF']
        email = request.form['email'].lower()
        senha = request.form['senha']

        usuario = Usuario(nome, sobrenome, cpf, idade, email, senha)
        if not usuarios.lista.get(email):
            usuarios.criar(usuario)
        
        return redirect(url_for('index'))
    
    return render_template('auth/cadastro.html')