import yaml
from app import db
from app.models.vehicle import *

def load_yaml(filename):
    with open(f"app/seeds/vehicles_data/{filename}", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

def seed_vehicles(app):

    @app.cli.command("seed_cars")
    def seed():

        categories = load_yaml("categories.yaml")
        brands = load_yaml("brands.yaml")
        models = load_yaml("models.yaml")
        versions = load_yaml("versions.yaml")
        transmissions = load_yaml("transmissions.yaml")

        for category in categories['categories']:
            db.session.add(Category(**category))
        for brand in brands['brands']:
            db.session.add(Brand(**brand))
        for model in models['models']:
            db.session.add(Model(**model))
        for version in versions['versions']:
            db.session.add(Version(**version))
        for transmission in transmissions['transmissions']:
            db.session.add(Transmission(**transmission))

        db.session.commit()