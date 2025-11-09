from app import db

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    vehicles = db.relationship("Vehicle", back_populates="category")

class Brand(db.Model):
    __tablename__ = 'brand'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    models = db.relationship("Model", back_populates="brand")

class Model(db.Model):
    __tablename__ = 'model'
    id = db.Column(db.Integer, primary_key=True)
    
    brand_id = db.Column(db.Integer, db.ForeignKey("brand.id"))
    brand = db.relationship("Brand", back_populates="models")

    name = db.Column(db.String(100), unique=True)
    vehicles = db.relationship("Vehicle", back_populates="model")

class Version(db.Model):
    __tablename__ = 'version'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    vehicles = db.relationship("Vehicle", back_populates="version")

class Transmission(db.Model):
    __tablename__ = 'transmission'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    vehicles = db.relationship("Vehicle", back_populates="transmission")

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'))
    version_id = db.Column(db.Integer, db.ForeignKey('version.id'))
    transmission_id = db.Column(db.Integer, db.ForeignKey('transmission.id'))

    category = db.relationship("Category", back_populates="vehicles")
    model = db.relationship("Model", back_populates="vehicles")
    version = db.relationship("Version", back_populates="vehicles")
    transmission = db.relationship("Transmission", back_populates="vehicles")

    plate = db.Column(db.String(7), nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False)
    mileage = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Boolean(), nullable=False)
    rental_price = db.Column(db.Numeric(10, 2), nullable=False)