from app import db, create_app, get_user_datastore, bcrypt
from app.models.user import Role

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        user_datastore = get_user_datastore()
        if not user_datastore.find_user(email='abc@gmail.com'):
            hashed_password = bcrypt.generate_password_hash("abc12345").decode('utf-8')
            user = user_datastore.create_user(
                nome='Raphael',
                email='abc@gmail.com',
                password=hashed_password
            )
            user_datastore.find_or_create_role(name='gerente', descricao='Gerente do sistema')
            user_datastore.add_role_to_user(user, 'gerente')
            db.session.commit()

    app.run(debug=True)