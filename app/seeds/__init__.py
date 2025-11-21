from app.seeds.generate_users import seed_users
from app.seeds.generate_vehicles import seed_vehicles
from app.seeds.generate_branches import seed_branches
from app.seeds.generate_extras import seed_extras

def seed_init(app):
    seed_users(app)
    seed_vehicles(app)
    seed_branches(app)
    seed_extras(app)