from app import db, faker
from app.models import Address, Branch, BusinessHours
from app.seeds.yaml_operations import load_yaml
from random import randint
from datetime import datetime

def to_time(string): return datetime.strptime(string, "%H:%M").time() 

def seed_branches(app):

    @app.cli.command("seed_branches")
    def seed(qnt_addresses=10):

        #creates n fake addresses
        for _ in range (qnt_addresses):
            address = Address(
                uf="2", #fixing state to UF 
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

            branch = Branch(
                name=f"Agência {address.city} - Centro",
                address_id=address.id,
                phone_number=faker.service_phone_number()
            )

            hoursObjList = load_yaml('hours_data/hours.yaml')

            for hourInst in hoursObjList['hours']:
                branch.hours.append(
                    hour:=BusinessHours(
                        weekday=hourInst['weekday'],
                        opens_at=to_time(hourInst['opens_at']),
                        closes_at=to_time(hourInst['closes_at'])
                    )
                )
                print("Create hour:", hour)

            print("Create branch:", branch)

            db.session.add(branch)
            db.session.commit()