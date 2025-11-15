from app import db
from app.models import Extra

import yaml

def load_yaml(filename) -> dict:
    with open(f"app/seeds/extras_data/{filename}", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

def seed_extras(app):
    
    @app.cli.command("seed_extras")
    def seed():
        extrasObjList = load_yaml("extras.yaml")
        for extraObj in extrasObjList:
            extraInst = Extra(**extraObj)
            if not Extra.query.get(extraObj['id']):
                db.session.add(extraInst)
                print("Create extra:", repr(extraInst))
        db.session.commit()