from app.seeds.generate_users import seed_users
from app.seeds.generate_vehicles import seed_vehicles
from app.seeds.generate_branches import seed_branches
from app.seeds.generate_extras import seed_extras
import subprocess

def seed_all(app):
    @app.cli.command("seed_all")
    def seed():
        with app.app_context():
            print("Iniciando o seeding de todos os dados...")
            subprocess.run(["flask", "seed_users"], check=True)
            subprocess.run(["flask", "seed_vehicles"], check=True)
            subprocess.run(["flask", "seed_branches"], check=True)
            subprocess.run(["flask", "seed_extras"], check=True)

def seed_init(app):
    seed_users(app)
    seed_vehicles(app)
    seed_branches(app)
    seed_extras(app)
    seed_all(app)
    seed_all(app)