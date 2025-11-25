from flask import render_template, request, jsonify
from flask_login import login_required
from flask_security import roles_accepted
import cloudinary.uploader
from app.cloudinary_setup import cloudinary_config
from app.models import Category, Model, Brand, Version, Engine, Transmission, Feature, Vehicle
from app.blueprints.main import main_bp
from app import db

def register_new_instance(Entity, atributes: dict):
    inst = Entity(**atributes)
    db.session.add(inst)
    db.session.commit()
    return inst.id

@main_bp.route('/dashboard/register-vehicles', methods=['GET', 'POST'])
@login_required
@roles_accepted('manager', 'worker')
def register_vehicles():
    categories = Category.query.all()
    models = Model.query.all()
    brands = Brand.query.all()
    versions = Version.query.all()
    features = Feature.query.all()
    transmissions = Transmission.query.all()

    if request.method == 'POST':

        try:

            #Category
            category_data = request.form['categories-category-id']
            if category_data.startswith("NEW:"):
                category_id = register_new_instance(Category, {'name' : category_data.removeprefix("NEW:")})
            else:
                category_id = int(category_data)

            #Brand
            brand_data = request.form['brands-brand-id']
            if brand_data.startswith("NEW:"):
                brand_id = register_new_instance(Brand, {'name' : brand_data.removeprefix("NEW:")})
            else:
                brand_id = int(brand_data)

            #Model
            model_data = request.form['models-model-id']
            if model_data.startswith("NEW:"):
                model_id = register_new_instance(Model, {'name' : model_data.removeprefix("NEW:")})
                model = Model.query.get(model_id)
                model.brand = Brand.query.get(brand_id)
                db.session.commit()
            else:
                model_id = int(model_data)
                model = Model.query.get(model_id)
            
            year = int(request.form['year'])

            #Version
            version_data = request.form['versions-version-id']
            if version_data.startswith("NEW:"):
                version_id = register_new_instance(Version, {'name' : version_data.removeprefix("NEW:")})
            else:
                version_id = int(version_data)

            #Transmission
            transmission_id = int(request.form['transmission'])

            #Engine
            displacement = float(request.form['displacement'])
            fuel = request.form['fuel']
            engine = Engine.query.filter_by(displacement=displacement, fuel=fuel).first()
            if not engine:
                engine_id = register_new_instance(Engine, {
                    'displacement' : displacement,
                    'fuel' : fuel
                })
            else:
                engine_id = engine.id

            feature_ids = request.form.getlist('features')
            features = [Feature.query.get(id) for id in feature_ids]

            plate = request.form['plate']
            mileage = request.form['mileage']
            n_people = request.form['n-people']
            daily_price = request.form['daily-price']

            cloudinary_config()

            img_file = request.files["img-file"]
            ext = img_file.filename.rsplit('.', 1)[-1].lower()

            cloudinary.uploader.upload(
                img_file,
                upload_preset="ClickAndDrive_preset",
                folder="ClickAndDrive",
                public_id=f"{model.brand.name}-{model.name}",
                use_filename=False,
                unique_filename=False,
                overwrite=True,
                resource_type="image",
                format=ext
            )

            new_vehicle = Vehicle(
                category_id=category_id,
                model_id=model_id,
                version_id=version_id,
                transmission_id=transmission_id,
                engine_id=engine_id,
                features=features,

                plate=plate,
                year=year,
                mileage=mileage,
                n_people=n_people,
                daily_price=daily_price,
                img_public_id=f"{model.brand.name}-{model.name}",
            )

            db.session.add(new_vehicle)
            db.session.commit()
            
            return jsonify({
                "success" : True,
                "message" : "Veículo cadastrado com sucesso",
                "icon" : "success"
            })
        
        except Exception as e:
            print("Erro ao cadastrar veículo", e)
            return jsonify({
                "success" : True,
                "message" : "Falha ao cadastrar veículo",
                "icon" : "error"
            })

    return render_template('main/register-vehicles.html', categories=categories, models=models, brands=brands, versions=versions, transmissions=transmissions, features=features)