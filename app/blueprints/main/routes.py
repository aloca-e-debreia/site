from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from flask_security import roles_accepted
from app.blueprints.main import main_bp
from app.models import User, select_users_with_role
from app.models import Vehicle, Feature
from app.models import Pickup, Dropoff
from app.models import Address
from app import login_manager, user_datastore, db

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    addresses = Address.query.all()

    if request.method == 'POST':
        pickup_address_id = request.form['pickup-address-id']
        pickup_date = request.form['pickup-date']
        pickup_time = request.form['pickup-time']

        dropoff_address_id = request.form['dropoff-address-id']
        dropoff_date = request.form['dropoff-date']
        dropoff_time = request.form['dropoff-time']

        pickup = Pickup(
            address_id=pickup_address_id,
            date=pickup_date,
            time=pickup_time
        )

        dropoff = Dropoff(
            address_id=dropoff_address_id,
            date=dropoff_date,
            time=dropoff_time
        )
        print(pickup, dropoff)
        return redirect(url_for('main.cars'))

    return render_template('main/index.html', current_user=current_user, addresses=addresses)

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
@login_required
def cars():
    vehicles = Vehicle.query.all()
    return render_template('main/cars.html', vehicles=vehicles)