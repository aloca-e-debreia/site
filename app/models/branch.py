from app import db

class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100), nullable=False, default='Brasil')
    state = db.Column(db.String(2), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(100), nullable=False)
    complement = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(12), nullable=False)

    def __repr__(self):
        return f"<Address(state='{self.state}', city='{self.city}', district='{self.district}', street='{self.street}', number='{self.number}', complement='{self.complement}', postal_code='{self.postal_code}')>"
    
    def name(self):
        return f"{self.street}, {self.number} - {self.state }, {self.district}"
    
class BusinessHours(db.Model):
    __tablename__ = 'business_hours'
    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey("branch.id"), nullable=False)

    weekday = db.Column(db.Integer, nullable=False) #0:Monday, 6:Saturday
    opens_at = db.Column(db.Time, nullable=False)
    closes_at = db.Column(db.Time, nullable=False)

    branch = db.relationship("Branch", back_populates="hours")

    def __repr__(self):
        return f"<BusinessHours(weekday='{self.weekday}', opens_at='{self.opens_at}', closes_at='{self.closes_at}')>"


class Branch(db.Model):
    __tablename__ = 'branch'
    id = db.Column(db.Integer, primary_key=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False, unique=True)
    
    name = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.String(11), nullable=False)
    
    address = db.relationship("Address", backref='branch')
    hours = db.relationship("BusinessHours", back_populates='branch', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Branch(address_id='{self.address_id}', name='{self.name}', phone_number='{self.phone_number}')>"