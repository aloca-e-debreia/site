from app import db, create_app, create_roles

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
        create_roles()

        from app.seeds import seed_init

        seed_init()

    app.run()