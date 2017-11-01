import sys
from sqlalchemy import Column, ForeignKey, Integer, String, \
    create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Customer(Base):

    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Facility(Base):

    __tablename__ = 'facility'

    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    customer = relationship(Customer)


class Device(Base):

    __tablename__ = 'device'

    id = Column(Integer, primary_key=True)
    device_type = Column(String, nullable=False)
    location_description = Column(String)
    facility_id = Column(Integer, ForeignKey('facility.id'))
    facility = relationship(Facility)


class Data(Base):

    __tablename__ = 'data'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    t1 = Column(Float)
    t2 = Column(Float)
    t3 = Column(Float)
    power = Column(Float)
    operation = Column(String(4), nullable=False)
    fan_on = Column(Boolean, nullable=False)
    device_id = Column(Integer, ForeignKey('device.id'))
    device = relationship(Device)


engine = create_engine('postgresql://catalog:catalog@localhost:5432/acmonitor')
Base.metadata.create_all(engine)