import yaml
from app import db, faker
from app.models.vehicle import *

def load_yaml(filename) -> dict:
    with open(f"app/seeds/vehicles_data/{filename}", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

def create_instances_from_yaml(objList: dict, inst_name: str, Entity) -> None:
    for obj in objList[inst_name]:
        instance = Entity(**obj)
        if not Entity.query.get(instance.id):
            db.session.add(instance)
            db.session.commit()
            print (f"Create {inst_name}:", repr(instance))

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
            objList = load_yaml(name+".yaml")
            create_instances_from_yaml(objList=objList, inst_name=name, Entity=entities[name])

        if Vehicle.query.first() == None:
            
            from random import choice, randint

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
                        features = [choice(features) for _ in range (5)],

                        plate = faker.license_plate(),
                        year = randint(1990, 2025),
                        mileage = float(randint(0, 2000)),
                        rental_price = float(randint(600, 2000)),
                    )
                    db.session.add(vehicle)
                    print("Create vehicle:", repr(vehicle))

            db.session.commit()