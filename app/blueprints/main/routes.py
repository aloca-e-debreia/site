from flask import render_template, request, jsonify, redirect, url_for, make_response
from flask_login import login_required, current_user
from flask_security import roles_accepted
from datetime import date, time
from app.blueprints.main import main_bp
from app.models import User, select_users_with_role, Vehicle, Feature, Address, Pickup, Dropoff, Extra, Rental, RentalExtra
from app import login_manager, user_datastore, db

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    addresses = Address.query.all()

    if request.method == 'POST':
        pickup_year, pickup_month, pickup_day = list(map(int, request.form['pickup-date'].split('-')))
        dropoff_year, dropoff_month, dropoff_day = list(map(int, request.form['dropoff-date'].split('-')))

        pickup_hour, pickup_min = list(map(int, request.form['pickup-time'].split(':')))
        dropoff_hour, dropoff_min = list(map(int, request.form['dropoff-time'].split(':')))

        pickup = Pickup(
            address_id=request.form['pickup-address-id'],
            date=date(pickup_year, pickup_month, pickup_day),
            time=time(pickup_hour, pickup_min)
        )

        dropoff = Dropoff(
            address_id=request.form['dropoff-address-id'],
            date=date(dropoff_year, dropoff_month, dropoff_day),
            time=time(dropoff_hour, dropoff_min)
        )
        
        db.session.add_all([pickup, dropoff])
        db.session.commit()

        resp = make_response(redirect(url_for('main.cars')))
        resp.set_cookie('pickup_id', str(pickup.id), max_age=60*60*24)
        resp.set_cookie('dropoff_id', str(dropoff.id), max_age=60*60*24)
        return resp

    return render_template('main/index.html', current_user=current_user, addresses=addresses)


@main_bp.route('/cars', methods=['GET', 'POST'])
@login_required
def cars():
    pickup_id = request.cookies.get('pickup_id')
    dropoff_id = request.cookies.get('dropoff_id')

    if not pickup_id or not dropoff_id:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        vehicle_id = request.form['vehicle-to-rent']

        rental = Rental(
            pickup_id=pickup_id,
            dropoff_id=dropoff_id,
            user_id=current_user.id,
            vehicle_id=vehicle_id,
            fee=0.12
        )

        db.session.add(rental)
        db.session.commit()

        resp = make_response(redirect(url_for('main.pay')))
        resp.set_cookie('vehicle_id', str(vehicle_id), max_age=60*60*24)
        resp.set_cookie('rental_id', str(rental.id), max_age=60*60*24)
        return resp

    vehicles = Vehicle.query.all()
    return render_template('main/cars.html', current_user=current_user, pickup_id=int(pickup_id), dropoff_id=int(dropoff_id), vehicles=vehicles)

@main_bp.route('/pay', methods=['GET', 'POST'])
def pay():
    pickup_id = request.cookies.get('pickup_id')
    dropoff_id = request.cookies.get('dropoff_id')
    vehicle_id = request.cookies.get('vehicle_id')
    rental_id = request.cookies.get('rental_id')

    if not pickup_id or not dropoff_id:
        return redirect(url_for('main.index'))
    
    if not vehicle_id or not rental_id:
        return redirect(url_for('main.cars'))

    extras = Extra.query.all()

    pickup = Pickup.query.get(int(pickup_id))
    dropoff = Dropoff.query.get(int(dropoff_id))
    vehicle = Vehicle.query.get(int(vehicle_id))
    rental = Rental.query.get(int(rental_id))

    if request.method == 'POST':
        extra = Extra.query.get(int(request.form['extra_id']))
        quantity = request.form['quantity']

        rental_extra = RentalExtra(extra=extra, quantity=int(quantity))

        rental.extras.append(rental_extra)

        db.session.commit()

        print(rental.extras)

    return render_template('main/pay.html', pickup=pickup, dropoff=dropoff, vehicle=vehicle, extras=extras)

@main_bp.route('/confirmation')
def confirmation():
    
    pickup_id = request.cookies.get('pickup_id')
    dropoff_id = request.cookies.get('dropoff_id')
    vehicle_id = request.cookies.get('vehicle_id')
    # rental = request.cookies.get('vehicle_id')

    if not pickup_id or not dropoff_id:
        return redirect(url_for('main.index'))
    
    if not vehicle_id:
        return redirect(url_for('main.cars'))

    pickup = Pickup.query.get(pickup_id)
    dropoff = Pickup.query.get(dropoff_id)
    vehicle = Vehicle.query.get(vehicle_id)

    return render_template('main/confirmation.html', pickup=pickup, dropoff=dropoff, vehicle=vehicle) #rental=rental)








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
