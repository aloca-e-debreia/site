from app import db

## NAMING

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    vehicles = db.relationship("Vehicle", back_populates="category")
    
    def __repr__(self):
        return f"<Category(name='{self.name}')>"

class Brand(db.Model):
    __tablename__ = 'brand'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    models = db.relationship("Model", back_populates="brand")

    def __repr__(self):
        return f"<Brand(name='{self.name}')>"

class Model(db.Model):
    __tablename__ = 'model'
    id = db.Column(db.Integer, primary_key=True)
    
    brand_id = db.Column(db.Integer, db.ForeignKey("brand.id"))
    brand = db.relationship("Brand", back_populates="models")

    name = db.Column(db.String(100), unique=True)
    vehicles = db.relationship("Vehicle", back_populates="model")

    def __repr__(self):
        return f"<Model(name='{self.name}', brand_id={self.brand_id})>"

class Version(db.Model):
    __tablename__ = 'version'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    vehicles = db.relationship("Vehicle", back_populates="version")

    def __repr__(self):
        return f"<Version(name='{self.name}')>"

## MECHANICAL

class Transmission(db.Model):
    __tablename__ = 'transmission'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    vehicles = db.relationship("Vehicle", back_populates="transmission")

    def __repr__(self):
        return f"<Transmission(name='{self.name}')>"

class Engine(db.Model):
    __tablename__ = 'engine'
    id = db.Column(db.Integer, primary_key=True)
    displacement = db.Column(db.String(100), nullable=False)
    fuel = db.Column(db.String(100), nullable=False)

    vehicles = db.relationship("Vehicle", back_populates="engine")

    def __repr__(self):
        return f"<Engine(displacement='{self.displacement}'), fuel='{self.fuel}'>"

## ASSOCIATIVE

class Feature(db.Model):
    __tablename__ = 'feature'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Feature(name='{self.name}')>"

vehicle_feature = db.Table(
    'vehicle_feature',
    db.Column('vehicle_id', db.Integer, db.ForeignKey('vehicle.id'), primary_key=True),
    db.Column('feature_id', db.Integer, db.ForeignKey('feature.id'), primary_key=True)
)

## VEHICLE

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'))
    version_id = db.Column(db.Integer, db.ForeignKey('version.id'))
    transmission_id = db.Column(db.Integer, db.ForeignKey('transmission.id'))
    engine_id = db.Column(db.Integer, db.ForeignKey('engine.id'))

    category = db.relationship("Category", back_populates="vehicles")
    model = db.relationship("Model", back_populates="vehicles")
    version = db.relationship("Version", back_populates="vehicles")
    transmission = db.relationship("Transmission", back_populates="vehicles")
    engine = db.relationship("Engine", back_populates="vehicles")

    features = db.relationship("Feature", secondary=vehicle_feature, backref="vehicle")

    plate = db.Column(db.String(7), nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False)
    mileage = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Boolean(), default=True, nullable=False)
    daily_price = db.Column(db.Numeric(10, 2), nullable=False)
    img_public_id = db.Column(db.String(200), nullable=False)
    n_people = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Vehicle(category_id={self.category_id},\
            model_id={self.model_id}, version_id={self.version_id},\
            transmission_id={self.transmission_id}, engine_id={self.engine_id}, \
            plate='{self.plate}', year='{self.year}', \
            mileage='{self.mileage}', daily_price='{self.daily_price}'>,\
            img_public_id={self.img_public_id}"
    
    def name(self):
        return f"{self.model.brand.name} {self.model.name} {self.engine.displacement} {self.version.name} {self.year}"
    
    from cloudinary import CloudinaryImage

    def get_img_url(self):
        from app.cloudinary_setup import cloudinary_config
        from cloudinary import CloudinaryImage
        cloudinary_config()
        return CloudinaryImage(self.img_public_id).build_url()