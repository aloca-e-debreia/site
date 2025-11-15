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
    
class Branch(db.Model):
    __tablename__ = 'branch'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), unique=True)

    address = db.relationship("Address", backref='branch')