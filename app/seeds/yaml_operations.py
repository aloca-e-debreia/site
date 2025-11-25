from app import db
import yaml

def load_yaml(filename) -> dict:
    with open(f"app/seeds/{filename}", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)
    
def create_instances_from_yaml(objList: dict, inst_name: str, Entity) -> None:

    existing_ids = {e.id for e in Entity.query.all() if getattr(e, "id", None) is not None} #fixing data duplication 

    existing_names = (
        {e.name for e in Entity.query.all() if hasattr(Entity, "name")}
        if hasattr(Entity, "name")
        else set()
    )

    created_count = 0


    for obj in objList[inst_name]:

        yaml_id = obj.get("id")

        #fixing ID duplication 
        if yaml_id is not None and yaml_id in existing_ids:
            continue

            #checking field "name" too

        if hasattr (Entity, "name"):
            yaml_name = obj.get("name")
            if yaml_name in existing_names:
                continue


        instance = Entity(**obj)
        db.session.add(instance)
        created_count += 1

        #fixing duplications within seeds

        if yaml_id is not None:
                existing_ids.add(yaml_id)
            
        if hasattr(Entity, "name") and obj.get("name"):
            existing_names.add(obj.get("name"))
                

    

    db.session.commit() #identation fix
    print (f"Create {inst_name}:", (created_count))