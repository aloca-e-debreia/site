from flask import Blueprint, request, redirect, url_for, render_template, make_response, jsonify
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
        usuario = Usuario(usuarios.next_id, nome, sobrenome, cpf, idade, email, senha)
        usuarios.criar(usuario)
        resposta = make_response(redirect(url_for('index')))
        resposta.set_cookie('usuario', usuario.nome, max_age=60*30)
        return resposta
    
    return render_template('auth/cadastro.html')

@cadastro_bp.route('/cadastro/api/cpf-existente', methods=['GET', 'POST'])
def verificar_cpf_existente():
    data = request.get_json()
    cpf = data.get("cpf")
    if cpf in usuarios.cpfs: return jsonify({"success" : False, "message" : "Já existe um usuário com mesmo CPF"})
    return jsonify({'success' : True, "message" : "Usuário cadastrado com sucesso"})