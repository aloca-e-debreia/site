from app import db
from datetime import date

class Pickup(db.Model):
    __tablename__ = 'pickup'

    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    branch = db.relationship("Branch", backref='pickup')

    def __repr__(self):
        return f"Pickup<id='{self.id}', branch_id='{self.branch_id}', date='{self.date}', time='{self.time}'>"

class Dropoff(db.Model):
    __tablename__ = 'dropoff'

    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    branch = db.relationship("Branch", backref='dropoff')

    def __repr__(self):
        return f"Dropoff<id='{self.id}', branch_id='{self.branch_id}', date='{self.date}', time='{self.time}'>"

class Extra(db.Model):
    __tablename__ = 'extra'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    daily_price = db.Column(db.Numeric(10, 2), nullable=False)
    selectable_quantity = db.Column(db.Boolean, nullable=False)

    rentals = db.relationship("RentalExtra", back_populates="extra")

    def __repr__(self):
        return f"Extra<name='{self.name}', description='{self.description}', daily_price='{self.daily_price}', quantity='{self.selectable_quantity}'>"

class RentalExtra(db.Model):
    __tablename__ = "rental_extra"

    id = db.Column(db.Integer, primary_key=True)

    rental_id = db.Column(db.Integer, db.ForeignKey('rental.id'))
    extra_id = db.Column(db.Integer, db.ForeignKey('extra.id'))

    quantity = db.Column(db.Integer, default=1)

    rental = db.relationship("Rental", back_populates="rental_extras")
    extra = db.relationship("Extra", back_populates="rentals")

    def calculate_price(self):
        return self.extra.daily_price * self.quantity
    

class Rental(db.Model):
    __tablename__ = 'rental'

    id = db.Column(db.Integer, primary_key=True)
    fee_decimal = db.Column(db.Numeric(10, 2), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    pickup_id = db.Column(db.Integer, db.ForeignKey('pickup.id'))
    dropoff_id = db.Column(db.Integer, db.ForeignKey('dropoff.id'))
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))

    vehicle = db.relationship("Vehicle", backref='rentals')
    pickup = db.relationship("Pickup", backref='rental')
    dropoff = db.relationship("Dropoff", backref='rental')
    branch = db.relationship("Branch", backref='rental')

    rental_extras = db.relationship("RentalExtra", back_populates='rental', cascade="all, delete-orphan")

    def __repr__(self):
        return f"Rental<user_id='{self.user_id}', vehicle_id='{self.vehicle_id}', pickup_id='{self.pickup_id}', dropoff_id='{self.dropoff_id}'>"
    
    def extras_daily_price(self):
        return sum(extra.calculate_price() for extra in self.rental_extras)

    def subtotal(self):
        days = (self.dropoff.date - self.pickup.date).days
        return days * (self.vehicle.daily_price + self.extras_daily_price())

    def total(self):
        return  f"{self.subtotal() * (1 + self.fee_decimal):.2f}"