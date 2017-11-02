from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_mapper import Base, Customer, Facility, Device, Data 


engine = create_engine('postgresql://catalog:catalog@localhost:5432/acmonitor')
# Class definitions connect to tables in db
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)

session = DBSession()
myFirstCustomer = Customer(name = "Bowditch Navigation")
CustomersFacility = Facility(address = "2300 Greenhill Dr, Ste 100 Round Rock, Texas 78664 USA", customer = myFirstCustomer)
# adds to the staging zone
session.add(myFirstCustomer)
session.commit()
print session.query(Customer).all()
print session.query(Facility).all()