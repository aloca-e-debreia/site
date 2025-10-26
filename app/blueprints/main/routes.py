from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from flask_security import roles_accepted
from app.blueprints.main import main_bp
from app.models.user import Usuario, select_users_with_role
from app import login_manager, user_datastore, db

@login_manager.user_loader
def load_user(usuario_id):
    return Usuario.query.get(int(usuario_id))

@main_bp.route('/')
def index():
    return render_template('main/index.html', current_user=current_user)

@main_bp.route('/dashboard')
@login_required
@roles_accepted('manager', 'worker')
def dashboard():
    clients = select_users_with_role('client')
    if current_user.has_role('manager'):
        workers, managers = select_users_with_role('worker'), select_users_with_role('manager')
        return render_template('main/dashboard.html', usuario_funcao='Gerente', clients=clients, workers=workers, managers=managers)
    else:
        return render_template('main/dashboard.html', usuario_funcao='Funcionário', clients=clients, workers=None, managers=None)
    
@main_bp.route('/dashboard/api/promover', methods=['GET', 'POST'])
def promover_usuario():
    data = request.get_json()
    
    usuarioID = data.get("id")
    usuarioFuncao = data.get("funcao")
    promocao = data.get("promocao")

    usuario = Usuario.query.get(int(usuarioID))
    if usuario:
        user_datastore.remove_role_from_user(usuario, usuarioFuncao)
        user_datastore.add_role_to_user(usuario, promocao)

        db.session.commit()

        return jsonify({"success" : True, "message" : "Usuário promovido com sucesso"})
    
    return jsonify({"success" : False, "message" : "Usuário não cadastrado"})