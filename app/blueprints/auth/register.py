from flask import request, redirect, url_for, render_template, jsonify, flash
from flask_login import login_user, login_required, current_user
from app.blueprints.auth import auth_bp
from app.models.user import User
from app import db, bcrypt, user_datastore

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name'].lower().capitalize()
        email = request.form['email'].lower()
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if not user: #precisa implementar checagem de email existente!
            user = User (
                name=name,
                email=email,
                password=bcrypt.generate_password_hash(password).decode('utf-8')
            )
            user_datastore.add_role_to_user(user, 'client')

            db.session.add(user)
            db.session.commit()

        login_user(user)
        return redirect(url_for('main.index'))
    
    return render_template('auth/register.html')

@auth_bp.route('/user/register-update', methods=['GET', 'POST'])
@login_required
def register_update():
    if request.method == 'POST':
        name = request.form['name'].lower().capitalize()
        age = int(request.form['age'])
        cpf = request.form['CPF']
        email = request.form['email'].lower()

        user = User.query.filter_by(email=email).first()
        if user:
            user.name = name
            user.age = age
            user.cpf = cpf
            user.email = email

            db.session.commit()
            login_user(user)

            flash("Dados atualizados com sucesso")
        else:
            flash("Usuário não encontrado")

    return render_template('auth/register-update.html', current_user=current_user)

@auth_bp.route('/register/api/existant-cpf', methods=['GET', 'POST'])
def verify_existant_cpf():
    data = request.get_json()
    cpf = data.get("cpf")
    email = data.get("email")
    user = User.query.filter_by(cpf=cpf).first()
    if user and user.email != email:
        return jsonify({"success" : False, "message" : "Já existe um usuário com mesmo CPF"})
    return jsonify({'success' : True, "message" : "Usuário cadastrado com sucesso"})