from flask import request, redirect, url_for, render_template, jsonify, flash
from flask_login import login_user, login_required, current_user
from app.blueprints.auth import auth_bp
from app.models.user import Usuario
from app import db, bcrypt, user_datastore

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome'].lower().capitalize()
        email = request.form['email'].lower()
        password = request.form['password']

        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario: #precisa implementar checagem de email existente!
            usuario = Usuario (
                nome=nome,
                email=email,
                password=bcrypt.generate_password_hash(password).decode('utf-8')
            )
            user_datastore.add_role_to_user(usuario, 'client')

            db.session.add(usuario)
            db.session.commit()

        login_user(usuario)
        return redirect(url_for('main.index'))
    
    return render_template('auth/cadastro.html')

@auth_bp.route('/usuario/registration', methods=['GET', 'POST'])
@login_required
def register_update():
    if request.method == 'POST':
        nome = request.form['nome'].lower().capitalize()
        idade = int(request.form['idade'])
        cpf = request.form['CPF']
        email = request.form['email'].lower()

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            usuario.nome = nome
            usuario.idade = idade
            usuario.cpf = cpf
            usuario.email = email

            db.session.commit()
            login_user(usuario)

            flash("Dados atualizados com sucesso")
        else:
            flash("Usuário não encontrado")

    return render_template('auth/register-update.html', current_user=current_user)

@auth_bp.route('/cadastro/api/cpf-existente', methods=['GET', 'POST'])
def verificar_cpf_existente():
    data = request.get_json()
    cpf = data.get("cpf")
    email = data.get("email")
    usuario = Usuario.query.filter_by(cpf=cpf).first()
    if usuario and usuario.email != email:
        return jsonify({"success" : False, "message" : "Já existe um usuário com mesmo CPF"})
    return jsonify({'success' : True, "message" : "Usuário cadastrado com sucesso"})