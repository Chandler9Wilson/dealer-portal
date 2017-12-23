# this assumes that
'''
CREATE DATABASE acmonitor;
CREATE USER catalog WITH PASSWORD 'catalog';
GRANT ALL PRIVILEGES ON DATABASE acmonitor TO catalog;
'''
# has been run
# also for SELECT privileges https://serverfault.com/a/284278
# TODO improve security for deployment
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, \
    Float, Boolean, DateTime, create_engine
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
    # Reguraly collected data will be constantly hit with updates

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


# Start user related tables


class User(Base):
    # A user of the website

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, nullable=False)
    profile_pic = Column(String)
    oauth_provider = Column(String, nullable=False)


class UserToFacility(Base):
    # A workers relationship to a facility to be used with permissions

    __tablename__ = 'user_to_facility'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    facility_id = Column(Integer, ForeignKey('facility.id'))
    facility = relationship(Facility)


class Role(Base):
    # This design might need a revision currently
    # a join will be needed everytime a role is pulled

    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    title = Column(String(20), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


engine = create_engine('postgresql://catalog:catalog@localhost:5432/acmonitor')
Base.metadata.create_all(engine)
