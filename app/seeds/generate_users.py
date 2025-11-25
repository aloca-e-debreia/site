from app import get_user_datastore, bcrypt, db, faker
from random import randint
import hashlib

def seed_users(app):

    @app.cli.command("seed_users")
    def seed(qnt_users=10):

        user_datastore = get_user_datastore()
        #creates n fake users
        roles = qnt_users//2*['client'] + qnt_users//2*['worker']
        if len(roles) != qnt_users: roles.append('worker')
        for _ in range (qnt_users):
            name = faker.first_name()
            first_name = name.lower().split()[0]
            email = f"{first_name}{randint(100, 999)}@test.com"
            hashed_email = hashlib.sha256(email.encode()).hexdigest()
            cpf = faker.cpf()
            if not user_datastore.find_user(email_hash=hashed_email):
                hashed_password = bcrypt.generate_password_hash(f"{first_name}{12345}").decode('utf-8')
                user = user_datastore.create_user(
                    name=name,
                    email=email,
                    password=hashed_password,
                    cpf=cpf
                )
                user_datastore.add_role_to_user(user, roles.pop())
            print(user)
                

        #create the manager
        email = "abc@gmail.com"
        hashed_email = hashlib.sha256("abc@gmail.com".encode()).hexdigest()
        if not user_datastore.find_user(email_hash=hashed_email):
            manager = user_datastore.create_user(
                name = "Raphael Vicente",
                email = email,
                password = bcrypt.generate_password_hash("abc12345").decode('utf-8'),
                cpf = "08199671068"
            )
            user_datastore.add_role_to_user(manager, "manager")
            print("Create manager:", manager)

        db.session.commit()