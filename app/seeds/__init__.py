from app.seeds.generate_users import seed_users
from app.seeds.generate_vehicles import seed_vehicles

def seed_init(app):
    seed_users(app)
    seed_vehicles(app)