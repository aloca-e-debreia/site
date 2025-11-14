from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from flask_security import roles_accepted
from app.blueprints.main import main_bp
from app.models.user import User, select_users_with_role
from app.models.vehicle import Vehicle, Feature
from app import login_manager, user_datastore, db

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main_bp.route('/')
def index():
    vehicles = Vehicle.query.all()
    return render_template('main/index.html', current_user=current_user, vehicles=vehicles)

@main_bp.route('/dashboard')
@login_required
@roles_accepted('manager', 'worker')
def dashboard():
    clients = select_users_with_role('client')
    if current_user.has_role('manager'):
        workers, managers = select_users_with_role('worker'), select_users_with_role('manager')
        return render_template('main/dashboard.html', user_role='Gerente', clients=clients, workers=workers, managers=managers)
    else:
        return render_template('main/dashboard.html', user_role='Funcionário', clients=clients, workers=None, managers=None)

@main_bp.route('/dashboard/register-vehicles')
@login_required
@roles_accepted('manager', 'worker')
def register_vehicles():
    features = Feature.query.all()
    return render_template('main/register-vehicles.html', features=features)

@main_bp.route('/dashboard/api/promote', methods=['GET', 'POST'])
def promover_user():
    data = request.get_json()
    
    user_id = data.get("id")
    user_role = data.get("role")
    promotion = data.get("promotion")

    user = User.query.get(int(user_id))
    if user:
        user_datastore.remove_role_from_user(user, user_role)
        user_datastore.add_role_to_user(user, promotion)

        db.session.commit()

        return jsonify({"success" : True, "message" : "Usuário promovido com sucesso"})
    
    return jsonify({"success" : False, "message" : "Usuário não cadastrado"})

@main_bp.route('/user')
def user():
    return render_template('main/user.html', current_user=current_user)

@main_bp.route('/user/<UserData_chosen>')
def UserData(UserData_chosen):
    return render_template('main/user.html', current_user=current_user, UserData_chosen=UserData_chosen)

@main_bp.route('/cars')
def cars():
    #precisa colocar os veiculos aqui
    return render_template('main/cars.html')