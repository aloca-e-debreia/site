from flask import request, redirect, url_for, render_template, make_response, jsonify
from app.blueprints.auth import auth_bp
from app.models.user import Usuario
from app import db

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome'].lower().capitalize()
        idade = int(request.form['idade'])
        cpf = request.form['CPF']
        email = request.form['email'].lower()
        senha = request.form['senha']

        if not Usuario.query.filter_by(email=email).first():
            usuario = Usuario(nome=nome, idade=int(idade), cpf=cpf, email=email, senha=senha)
            db.session.add(usuario)
            db.session.commit()

        resposta = make_response(redirect(url_for('main.index')))
        resposta.set_cookie('usuario', usuario.nome, max_age=60*30)
        return resposta
    
    return render_template('auth/cadastro.html')

@auth_bp.route('/cadastro/api/cpf-existente', methods=['GET', 'POST'])
def verificar_cpf_existente():
    data = request.get_json()
    cpf = data.get("cpf")
    if Usuario.query.filter_by(cpf=cpf).first():
        return jsonify({"success" : False, "message" : "Já existe um usuário com mesmo CPF"})
    return jsonify({'success' : True, "message" : "Usuário cadastrado com sucesso"})