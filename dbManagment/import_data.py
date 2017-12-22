import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_mapper import Base, Customer, Facility, Device, Data


engine = create_engine('postgresql://catalog:catalog@localhost:5432/acmonitor')
# Class definitions connect to tables in db
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def add_to_session(data):

    def facility_add(entry, customer):
        for facility in customer["facility"]:
            if "address" in facility:
                entry.facility = Facility(
                    address=facility["address"],
                    customer=entry.customer
                )
                session.add(entry.facility)
            else:
                return 'Error: please add an address for each facility'

    def device_add(entry, customer):
        for device in customer["device"]:
            if "device_type" in device:
                if "location_description" in device:
                    if "address" in device:
                        entry.device = Device(
                            device_type=device["device_type"],
                            location_description=device["location_description"],
                            facility=entry.facility
                        )
                        session.add(entry.device)
                    else:
                        return "incomplete device"
                else:
                    return "incomplete device"
            else:
                return "incomplete device"

    for customer in data:
        # this creates an empty obj
        entry = type('entry', (), {})()

        if "customer" in customer:
            if "name" in customer["customer"]:
                entry.customer = Customer(name=customer["customer"]["name"])
                session.add(entry.customer)

                facility_add(entry, customer)
                device_add(entry, customer)

                session.commit()

            else:
                return 'Error: please add a customer name'
        else:
                return 'Error: please add a customer'


# good explenation of with http://effbot.org/zone/python-with-statement.htm
with open('fake_data.JSON') as fake_data:
    data = json.load(fake_data)
    add_to_session(data)
