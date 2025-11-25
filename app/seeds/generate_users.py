from app import get_user_datastore, bcrypt, db, faker
from random import randint

def seed_users(app):

    @app.cli.command("seed_users")
    def seed(qnt_users=10):

        user_datastore = get_user_datastore()

        
        required_roles = ["client", "worker", "manager"]
        for role in required_roles:
            if not user_datastore.find_role(role):
                user_datastore.create_role(name=role)

        db.session.commit()

        #fix logic and syntax
        roles = (["client"] * (qnt_users // 2)) + (["worker"] * (qnt_users // 2))

        #fix logical
        if len(roles) < qnt_users:
            roles.append("worker")

        #fix syntax
        for _ in range(qnt_users):
            name = faker.name()
            first_name = name.lower().split()[0]
            email = f"{first_name}{randint(100,999)}@test.com"

            if not user_datastore.find_user(email=email):
                password = bcrypt.generate_password_hash(f"{first_name}12345").decode('utf-8')
                user = user_datastore.create_user(
                    name=name,
                    email=email,
                    password=password
                )
                user_datastore.add_role_to_user(user, roles.pop())
                print("Created user:", repr(user))

        
        if not user_datastore.find_user(email="abc@gmail.com"):
            manager = user_datastore.create_user(
                name="Raphael Vicente",
                email="abc@gmail.com",
                password=bcrypt.generate_password_hash("abc12345").decode("utf-8")
            )
            user_datastore.add_role_to_user(manager, "manager")
            print("Created manager:", repr(manager))

        db.session.commit()