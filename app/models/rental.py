from app import db

class Pickup(db.Model):
    __tablename__ = 'pickup'

    id = db.Column(db.Integer, primary_key=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    address = db.relationship("Address", backref='pickup')

    def __repr__(self):
        return f"Pickup<id='{self.id}', address_id='{self.address_id}', date='{self.date}', time='{self.time}'>"

class Dropoff(db.Model):
    __tablename__ = 'dropoff'

    id = db.Column(db.Integer, primary_key=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    address = db.relationship("Address", backref='dropoff')

    def __repr__(self):
        return f"Dropoff<id='{self.id}', address_id='{self.address_id}', date='{self.date}', time='{self.time}'>"

class Extra(db.Model):
    __tablename__ = 'extra'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    daily_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Boolean, nullable=False)

    rentals = db.relationship("Rental", secondary='rental_extra', back_populates='extras')

    def __repr__(self):
        return f"Extra<name='{self.name}', description='{self.description}', daily_price='{self.daily_price}', quantity='{self.quantity}', available='{self.available}'>"

rental_extra = db.Table(
    "rental_extra",
    db.Column("rental_id", db.Integer, db.ForeignKey('rental.id'), primary_key=True),
    db.Column("extra_id", db.Integer, db.ForeignKey('extra.id'), primary_key=True)
)

class Rental(db.Model):
    __tablename__ = 'rental'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    pickup_id = db.Column(db.Integer, db.ForeignKey('pickup.id'))
    dropoff_id = db.Column(db.Integer, db.ForeignKey('dropoff.id'))

    vehicle = db.relationship("Vehicle", backref='rentals')
    pickup = db.relationship("Pickup", backref='rental')
    dropoff = db.relationship("Dropoff", backref='rental')

    extras = db.relationship("Extra", secondary='rental_extra', back_populates='rentals')

    def __repr__(self):
        return f"Rental<user_id='{self.user_id}', vehicle_id='{self.vehicle_id}', pickup_id='{self.pickup_id}', dropoff_id='{self.dropoff_id}'>"