from app import db
import yaml

def load_yaml(filename) -> dict:
    with open(f"app/seeds/{filename}", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)
    
def create_instances_from_yaml(objList: dict, inst_name: str, Entity) -> None:
    for obj in objList[inst_name]:
        instance = Entity(**obj)
        if not Entity.query.get(instance.id):
            db.session.add(instance)
            db.session.commit()
            print (f"Create {inst_name}:", repr(instance))
