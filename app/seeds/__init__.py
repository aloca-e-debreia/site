from app.seeds.generate_users import seed_users

def seed_init(app):
    seed_users(app)