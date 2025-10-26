from app import db, create_app, get_user_datastore, create_roles, bcrypt

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        user_datastore = get_user_datastore()
        
        create_roles()

        if not user_datastore.find_user(email='abc@gmail.com'):
            hashed_password = bcrypt.generate_password_hash("abc12345").decode('utf-8')
            user = user_datastore.create_user(
                nome='Raphael',
                email='abc@gmail.com',
                password=hashed_password
            )
            user_datastore.add_role_to_user(user, 'manager')

        if not user_datastore.find_user(email='filipe@gmail.com'):
            hashed_password = bcrypt.generate_password_hash("filipe12345").decode('utf-8')
            user = user_datastore.create_user(
                nome='Filipe',
                email='filipe@gmail.com',
                password=hashed_password
            )
            user_datastore.add_role_to_user(user, 'worker')

        if not user_datastore.find_user(email='almir@gmail.com'):
            hashed_password = bcrypt.generate_password_hash("almir12345").decode('utf-8')
            user = user_datastore.create_user(
                nome='Almir',
                email='almir@gmail.com',
                password=hashed_password
            )
            user_datastore.add_role_to_user(user, 'client')

            db.session.commit()

    app.run(debug=True)