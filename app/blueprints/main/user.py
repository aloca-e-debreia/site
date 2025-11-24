from flask import render_template, request, jsonify
from flask_security import roles_accepted
from flask_login import login_required, current_user
from app.blueprints.main import main_bp
from app.models import User, select_users_with_role, Rental, RentalStatus
from app import db, get_user_datastore, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main_bp.route('/user')
@login_required
def user():
    return render_template('main/user.html', current_user=current_user)

@main_bp.route('/user/<UserData_chosen>')
def UserData(UserData_chosen):
    active_rents = Rental.query.filter(
        Rental.user_id == current_user.id,
        Rental.status.in_([RentalStatus.ACTIVE, RentalStatus.PENDING])
    ).all()
    finished_rents = Rental.query.filter(
        Rental.user_id == current_user.id,
        Rental.status.in_([RentalStatus.CLOSED, RentalStatus.CANCELED])
    ).all()

    return render_template('main/user.html', current_user=current_user, UserData_chosen=UserData_chosen, active_rents=active_rents, finished_rents=finished_rents)

@main_bp.route('/dashboard')
@login_required
@roles_accepted('manager', 'worker')
def dashboard():
    clients = select_users_with_role('client')
    if current_user.has_role('manager'):
        workers, managers = select_users_with_role('worker'), select_users_with_role('manager')
        return render_template('main/dashboardControll.html', user_role='Gerente', clients=clients, workers=workers, managers=managers)
    else:
        return render_template('main/dashboard.html', user_role='Funcionário', clients=clients, workers=None, managers=None)

@main_bp.route('listPerson')
@login_required
@roles_accepted('manager', 'worker')
def listPerson():
    return render_template('main/listperson.html')

@main_bp.route('/dashboard/api/promote', methods=['POST'])
def promover_user():
    if request.method == "POST" and request.is_json:
        data = request.get_json()

        user_id = int(data.get("id"))
        user_role = data.get("role")
        promotion = data.get("promotion")

        user = User.query.get(int(user_id))
        if user:
            user_datastore = get_user_datastore()
            user_datastore.remove_role_from_user(user, user_role)
            user_datastore.add_role_to_user(user, promotion)

            db.session.commit()

            return jsonify({"success" : True, "message" : "Usuário promovido com sucesso"})

        return jsonify({"success" : False, "message" : "Usuário não cadastrado"})

@main_bp.route('/user/2/api/cancel', methods=['GET', 'POST'])
def cancel_rent():
    data = request.get_json()

    active_rent_id = int(data.get("rentId"))
    active_rent = Rental.query.get(active_rent_id)
    if active_rent:
        active_rent.status = RentalStatus.CANCELED
        db.session.commit()

        return jsonify({
            "success" : True,
            "message" : "Locação cancelada com sucesso"
        })
    return jsonify({
            "success" : False,
            "message" : "Locação não encontrada"
        })