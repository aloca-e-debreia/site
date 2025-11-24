import yaml
from app import db, faker
from app.models import *
from app.seeds.yaml_operations import load_yaml, create_instances_from_yaml

def seed_vehicles(app):

    @app.cli.command("seed_vehicles")
    def seed():
        entities = {"categories" : Category,
                    "brands" : Brand,
                    "models" : Model,
                    "versions" : Version,
                    "transmissions" : Transmission,
                    "engines" : Engine,
                    "features" : Feature
                    }

        for name in entities:
            objList = load_yaml("vehicles_data/"+name+".yaml")
            if entities[name].query.count() == 0:
                create_instances_from_yaml(objList=objList, inst_name=name, Entity=entities[name])
            
        from random import choice, uniform, randint

        versions = [version.id for version in Version.query.all()]
        transmissions = [transmission.id for transmission in Transmission.query.all()]
        engines = [engine.id for engine in Engine.query.all()]
        features = [feature for feature in Feature.query.all()]

        for category in Category.query.all():
            for model in Model.query.all():
                vehicle = Vehicle(
                    category_id = category.id,
                    model_id = model.id,
                    version_id = choice(versions),
                    transmission_id = choice(transmissions),
                    engine_id = choice(engines),
                    features = list(set(choice(features) for _ in range(3))),

                    plate = faker.license_plate(),
                    year = randint(2000, 2025),
                    mileage = uniform(0, 1000),
                    daily_price = uniform(100, 490),
                    img_public_id = f"{model.brand.name}-{model.name}",
                    n_people = randint(1, 5)
                )
                db.session.add(vehicle)
                print("Create vehicle:", repr(vehicle))

            db.session.commit()