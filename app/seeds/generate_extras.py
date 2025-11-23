from app import db
from app.models import Extra
from app.seeds.yaml_operations import load_yaml, create_instances_from_yaml

def seed_extras(app):
    
    @app.cli.command("seed_extras")
    def seed():
        extrasObjList = load_yaml("extras_data/extras.yaml")
        create_instances_from_yaml(objList=extrasObjList, inst_name='extras', Entity=Extra)