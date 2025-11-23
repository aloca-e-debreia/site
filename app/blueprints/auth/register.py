from flask import request, redirect, url_for, render_template, jsonify, flash
from flask_login import login_user, login_required, current_user
from app.blueprints.auth import auth_bp
from app.models import User
from app import db, bcrypt, user_datastore, is_safe_url

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name'].lower().capitalize()
        email = request.form['email'].lower()
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if not user:
            user = User (
                name=name,
                email=email,
                password=bcrypt.generate_password_hash(password).decode('utf-8')
            )

            db.session.add(user)
            db.session.commit()

            user_datastore.add_role_to_user(user, 'client')
            db.session.commit()
            login_user(user)

            next_page = request.form['next'] or request.args.get("next")
            print(next_page)
            if not next_page or not is_safe_url(next_page):
                return redirect(url_for('main.index'))
            
            return redirect(next_page)
            
    
    return render_template('auth/register.html')

@auth_bp.route('/user/register-update', methods=['GET', 'POST'])
@login_required
def register_update():
    if request.method == 'POST':
        name = request.form['name'].lower().capitalize()
        age = int(request.form['age'])
        cpf = request.form['CPF']
        email = request.form['email'].lower()

        user = User.query.get(current_user.id)
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

    if current_user.is_authenticated: # register uptdate
        user_id = current_user.id
        existant_cpf = User.query.filter(User.cpf == cpf, User.id != user_id).first()
    else: # first access
        existant_cpf = User.query.filter_by(cpf=cpf).first()

    if existant_cpf:
        return jsonify({"success" : False, "message" : "Já existe um usuário com mesmo CPF"})
    return jsonify({'success' : True, "message" : "Usuário cadastrado com sucesso"})

@auth_bp.route('/register/api/existant-email', methods=['GET', 'POST'])
def verify_existant_email():
    data = request.get_json()
    email = data.get("email")

    if current_user.is_authenticated: #register update
        user_id = current_user.id
        existant_email = User.query.filter(User.email == email, User.id != user_id).first()
    else: # first access
        existant_email = User.query.filter_by(email=email).first()

    if existant_email:
        return jsonify({"success" : False, "message" : "Já existe um usuário com mesmo email"})
    return jsonify({'success' : True, "message" : "Usuário cadastrado com sucesso"})