from flask import request, redirect, url_for, render_template, jsonify
from flask_login import login_user
from app.blueprints.auth import auth_bp
from app.models.user import Usuario
from app import db
from app import bcrypt

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome'].lower().capitalize()
        idade = int(request.form['idade'])
        cpf = request.form['CPF']
        email = request.form['email'].lower()
        password = request.form['password']

        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario:
            usuario = Usuario (
                nome=nome,
                idade=int(idade),
                cpf=cpf,
                email=email,
                password=bcrypt.generate_password_hash(password).decode('utf-8')
            )
            db.session.add(usuario)
            db.session.commit()

        login_user(usuario)
        return redirect(url_for('main.index'))
    
    return render_template('auth/cadastro.html')

@auth_bp.route('/cadastro/api/cpf-existente', methods=['GET', 'POST'])
def verificar_cpf_existente():
    data = request.get_json()
    cpf = data.get("cpf")
    if Usuario.query.filter_by(cpf=cpf).first():
        return jsonify({"success" : False, "message" : "Já existe um usuário com mesmo CPF"})
    return jsonify({'success' : True, "message" : "Usuário cadastrado com sucesso"})