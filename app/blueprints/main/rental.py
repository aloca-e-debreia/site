from flask import render_template, request, redirect, url_for, make_response, jsonify
from flask_login import login_required, current_user
from datetime import date, time
from app.blueprints.main import main_bp
from app.models import Branch, Vehicle, Pickup, Dropoff, Extra, Rental, RentalExtra
from app import db

@main_bp.route('/api/resume/rent', methods=['POST'])
def resume_rent():
    if request.method == 'POST' and request.is_json:
        try:    
            data = request.get_json()
            confirm = data.get('confirmation')
            route = data.get('route')

            url = url_for(route)
            resp = jsonify({
                "success" : True,
                "redirect_url" : url
            })
            
            if not confirm:
                Rental.query.filter_by(id=request.cookies.get('rental_id')).delete()
                db.session.commit()
                for cookie in ['pickup_id', 'dropoff_id', 'vehicle_id', 'rental_id']:
                    resp.set_cookie(cookie, "", expires=0)

            return resp
        
        except Exception as e:

            print("Erro:", e)
            return jsonify({
                "success" : False,
                "message" : "Ocorreu um erro ao buscar sua locação... Tente novamente mais tarde."
            })

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    branches = Branch.query.all()

    if request.method == 'POST' and request.is_json:
        pickup_id = request.cookies.get('pickup_id')
        dropoff_id = request.cookies.get('dropoff_id')
        vehicle_id = request.cookies.get('vehicle_id')
        rental_id = request.cookies.get('rental_id')

        if vehicle_id and rental_id:
            return jsonify({
                "route" : "main.pay"
            })
        elif pickup_id and dropoff_id:
            return jsonify({
                "route" : "main.cars"
            })
        else:
            return jsonify({
                "route" : None
            })

    if request.method == 'POST':
        #pickup/dropoff branch
        pickup_branch_id = request.form['pickup-branch-id']

        dropoff_branch_id = request.form['dropoff-branch-id']

        #pickup/dropoff time
        pickup_year, pickup_month, pickup_day = list(map(int, request.form['pickup-date'].split('-')))
        dropoff_year, dropoff_month, dropoff_day = list(map(int, request.form['dropoff-date'].split('-')))

        pickup_hour, pickup_min = list(map(int, request.form['pickup-time'].split(':')))
        dropoff_hour, dropoff_min = list(map(int, request.form['dropoff-time'].split(':')))

        pickup = Pickup(
            branch_id=pickup_branch_id,
            date=date(pickup_year, pickup_month, pickup_day),
            time=time(pickup_hour, pickup_min)
        )

        dropoff = Dropoff(
            branch_id=dropoff_branch_id,
            date=date(dropoff_year, dropoff_month, dropoff_day),
            time=time(dropoff_hour, dropoff_min)
        )
        
        db.session.add_all([pickup, dropoff])
        db.session.commit()

        resp = make_response(redirect(url_for('main.cars')))
        resp.set_cookie('pickup_id', str(pickup.id), max_age=60*60*24)
        resp.set_cookie('dropoff_id', str(dropoff.id), max_age=60*60*24)
        return resp

    return render_template('main/index.html', branches=branches)


@main_bp.route('/cars', methods=['GET', 'POST'])
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
            vehicle_id=vehicle_id,
            fee_decimal=0.12
        )

        db.session.add(rental)
        db.session.commit()

        resp = make_response(redirect(url_for('main.pay')))
        resp.set_cookie('vehicle_id', str(vehicle_id), max_age=60*60*24)
        resp.set_cookie('rental_id', str(rental.id), max_age=60*60*24)
        return resp

    pickup = Pickup.query.get(int(pickup_id))
    dropoff = Dropoff.query.get(int(dropoff_id))
    vehicles = Vehicle.query.all()
    return render_template('main/cars.html', vehicles=vehicles, pickup=pickup, dropoff=dropoff)

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

        assoc = RentalExtra.query.filter_by(rental_id=rental_id, extra_id=extra.id).first()

        if not assoc: #if the location doesn't have the extra
            rental_extra = RentalExtra(rental=rental, extra=extra, quantity=int(quantity))
            db.session.add(rental_extra)
            rental.rental_extras.append(rental_extra)
        else:
            assoc.quantity = quantity

        db.session.commit()

    return render_template('main/pay.html', pickup=pickup, dropoff=dropoff, vehicle=vehicle, rental=rental, rental_extras=rental.rental_extras, extras=extras)

@main_bp.route('/confirmation', methods=['GET', 'POST'])
@login_required
def confirmation():
    
    pickup_id = request.cookies.get('pickup_id')
    dropoff_id = request.cookies.get('dropoff_id')
    vehicle_id = request.cookies.get('vehicle_id')
    rental_id = request.cookies.get('rental_id')

    if not pickup_id or not dropoff_id:
        return redirect(url_for('main.index'))
    
    if not vehicle_id or not rental_id:
        return redirect(url_for('main.cars'))

    if request.method == "POST":
        resp = make_response(redirect(url_for('main.index')))
        for cookie in ['pickup_id', 'dropoff_id', 'vehicle_id', 'rental_id']:
            resp.set_cookie(cookie, "", expires=0)
        return resp

    pickup = Pickup.query.get(int(pickup_id))
    dropoff = Dropoff.query.get(int(dropoff_id))
    vehicle = Vehicle.query.get(int(vehicle_id))
    rental = Rental.query.get(int(rental_id))

    rental.user_id = current_user.id

    db.session.commit()

    return render_template('main/confirmation.html', pickup=pickup, dropoff=dropoff, vehicle=vehicle, rental=rental, rental_extras=rental.rental_extras)