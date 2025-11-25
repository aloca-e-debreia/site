from flask import render_template, request, jsonify
from flask_security import roles_accepted
from flask_login import login_required, current_user
from app.blueprints.main import main_bp
from app.models import User, select_users_with_role, Rental, RentalStatus
from app import db, get_user_datastore, login_manager

# USER PORTAL

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main_bp.route('/user')
@login_required
def user():
    return render_template('main/user.html', current_user=current_user)

@main_bp.route('/user/<UserData_chosen>')
@login_required
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

@main_bp.route('/user/2/api/cancel', methods=['POST'])
@login_required
def cancel_rent():
    if request.method == 'POST' and request.is_json:
        data = request.get_json()

        active_rent_id = int(data.get("rentId"))
        active_rent = Rental.query.get(active_rent_id)
        if active_rent:
            active_rent.status = RentalStatus.CANCELED
            db.session.commit()

            return jsonify({
                "success" : True,
                "title" : "Locação cancelada com sucesso",
                "icon" : "success"
            })
        
        return jsonify({
                "success" : False,
                "title" : "Locação não encontrada",
                "icon" : "error"
            })

# DASHBOARD

@main_bp.route('/dashboard/clients')
@login_required
@roles_accepted('manager', 'worker')
def list_clients():
    clients = select_users_with_role('client')
    return render_template('main/listperson.html', list='clientes', list_role='client', users=clients)
    
@main_bp.route('/dashboard/workers')
@login_required
@roles_accepted('manager')
def list_workers():
    workers = select_users_with_role('worker')
    return render_template('main/listperson.html', list='funcionários', list_role='worker', users=workers)

@main_bp.route('/dashboard/managers')
@login_required
@roles_accepted('manager')
def list_managers():
    managers = select_users_with_role('manager')
    return render_template('main/listperson.html', list='gerentes', list_role='manager', users=managers)


@main_bp.route('dashboard/controll')
@login_required
@roles_accepted('manager', 'worker')
def dashboard_controll():
    return render_template('main/dashboardControll.html')

@main_bp.route('/dashboard/api/promote', methods=['POST'])
@login_required
@roles_accepted('worker', 'manager')
def promote_user():
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

            return jsonify({
                "success" : True,
                "title" : "Usuário promovido com sucesso",
                "icon" : "success"
            })

        return jsonify({
            "success" : False,
            "title" : "Usuário não cadastrado",
            "icon" : "error"
        })