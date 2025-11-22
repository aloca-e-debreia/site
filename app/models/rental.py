import enum
from app import db

class Pickup(db.Model):
    __tablename__ = 'pickup'

    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    branch = db.relationship("Branch", backref='pickup')

    @property
    def date_br(self):
        return self.date.strftime("%d/%m/%Y")

    def __repr__(self):
        return f"Pickup<id='{self.id}', branch_id='{self.branch_id}', date='{self.date}', time='{self.time}'>"

class Dropoff(db.Model):
    __tablename__ = 'dropoff'

    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    branch = db.relationship("Branch", backref='dropoff')

    @property
    def date_br(self):
        return self.date.strftime("%d/%m/%Y")

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

    @property
    def total(self):
        return self.extra.daily_price * self.quantity
    
class RentalStatus(enum.Enum):
    PENDING = "pending" #hasn't got the car 
    ACTIVE = "active" #got the car, ongoing status
    CLOSED = "closed" #returned the car
    CANCELED = 'canceled'
    LATE = "late"

class Rental(db.Model):
    __tablename__ = 'rental'

    id = db.Column(db.Integer, primary_key=True)
    fee_decimal = db.Column(db.Numeric(5, 4), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    pickup_id = db.Column(db.Integer, db.ForeignKey('pickup.id'), unique=True)
    dropoff_id = db.Column(db.Integer, db.ForeignKey('dropoff.id'), unique=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))

    user = db.relationship("User", backref='rentals')
    branch = db.relationship("Branch", backref='rental')
    pickup = db.relationship("Pickup", backref='rental', single_parent=True, uselist=False, cascade="all, delete-orphan")
    dropoff = db.relationship("Dropoff", backref='rental', single_parent=True, uselist=False, cascade="all, delete-orphan")
    vehicle = db.relationship("Vehicle", backref='rentals')

    rental_extras = db.relationship("RentalExtra", back_populates='rental', cascade="all, delete-orphan")

    status = db.Column(db.Enum(RentalStatus, name="rental_status"), nullable=False, default=RentalStatus.PENDING)

    @property
    def status_label(self):
        labels = {
            RentalStatus.PENDING: "Pendente",
            RentalStatus.ACTIVE: "Ativa",
            RentalStatus.CLOSED: "Concluída",
            RentalStatus.LATE: "Atrasada",
            RentalStatus.CANCELED: "Cancelada",
        }
        return labels.get(self.status, "Desconhecido")
    
    @property
    def days(self):
        if not self.dropoff or not self.pickup:
            return 0
        return max((self.dropoff.date - self.pickup.date).days, 1)
    
    @property
    def extras_daily_price(self):
        return sum(extra.total for extra in self.rental_extras)

    @property
    def extras_total(self):
        return self.extras_daily_price * self.days

    @property
    def vehicle_total(self):
        return self.vehicle.daily_price * self.days

    @property
    def subtotal(self):
        return self.extras_total + self.vehicle_total

    @property
    def fee_price(self):
        return self.subtotal * self.fee_decimal

    @property
    def total(self):
        return self.subtotal + self.fee_price
    
    def __repr__(self):
        return (
            f"Rental<user_id='{self.user_id}', vehicle_id='{self.vehicle_id}', "
            f"pickup_id='{self.pickup_id}', dropoff_id='{self.dropoff_id}', "
            f"branch_id='{self.branch_id}', status='{self.status}'>"
        )