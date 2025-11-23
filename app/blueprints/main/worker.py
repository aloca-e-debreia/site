from flask import render_template, request, jsonify
from flask_security import roles_accepted
from flask_login import login_required
from app.blueprints.main import main_bp
from app.models import Rental, RentalStatus
from app import db
from flask import session

@main_bp.route('/dashboard/api/alter/status', methods=['POST'])
def alter_rent_status():
    if request.method == 'POST' and request.is_json:
        try:
            data = request.get_json()
            rent_id = data.get("rent_id")
            new_status = data.get("new_status")
            rent = Rental.query.get(rent_id)
            rent.status = RentalStatus[new_status]

            db.session.commit()

            return jsonify({
                "success" : True,
                "message" : "Locação alterada com sucesso"            
            })
        
        except Exception as e:
            print("Erro ao alterar status da locação:", e)
            return jsonify({
                "success" : False,
                "message" : "Ocorreu algum erro na aplicação... Tente novamente mais tarde"
            })

@main_bp.route('/dashboard/rents/pending')
@login_required
@roles_accepted('manager', 'worker')
def pending_rents():
    pending_rents = Rental.query.filter_by(status=RentalStatus.PENDING).all()
    btn_class = "pending"
    btn_message = "Atestar retirada"
    return render_template('main/rents.html', rents=pending_rents, btn_class=btn_class, btn_message=btn_message)

@main_bp.route('/dashboard/rents/active')
@login_required
@roles_accepted('manager', 'worker')
def active_rents():
    active_rents = Rental.query.filter_by(status=RentalStatus.ACTIVE).all()
    btn_class = "active"
    btn_message = "Atestar devolução"
    return render_template('main/rents.html', rents=active_rents, btn_class=btn_class, btn_message=btn_message)

@main_bp.route('/dashboard/rents/late')
@login_required
@roles_accepted('manager', 'worker')
def late_rents():
    late_rents = Rental.query.filter_by(status=RentalStatus.LATE).all()
    btn_class = "late"
    btn_message = "Atestar devolução atrasada"
    return render_template('main/rents.html', rents=late_rents, btn_class=btn_class, btn_message=btn_message)