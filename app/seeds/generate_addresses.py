from app import db, faker
from app.models import Address
from random import randint

def seed_addresses(app):

    @app.cli.command("seed_addresses")
    def seed(qnt_addresses=10):

        #creates n fake addresses
        for _ in range (qnt_addresses):
            address = Address(
                state="São Paulo",
                city=faker.city(),
                street=faker.street_name(),
                number=randint(0, 2000),
                complement="house",
                district=faker.bairro(),
                postal_code=faker.postcode()
            )
            print("Create address:", repr(address))
            db.session.add(address)

        db.session.commit()