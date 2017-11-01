# this assumes that
'''
CREATE DATABASE acmonitor;
CREATE USER catalog WITH PASSWORD 'catalog';
GRANT ALL PRIVILEGES ON DATABASE acmonitor TO catalog;
'''
# has been run
import sqlalchemy
import datetime
from sqlalchemy import Table, Column, Integer, String, Float, \
    Boolean, ForeignKey, DateTime


# user, password should be added at some point
def connect(user, password, db, host='localhost', port=5432):
    '''Returns a connection and a metadata object'''

    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    # The return value of create_engine() is our connection object
    con = sqlalchemy.create_engine(url, client_encoding='utf8')

    # We then bind the connection to MetaData()
    meta = sqlalchemy.MetaData(bind=con, reflect=True)

    return con, meta


def setup():
    facility = Table(
        'facility', meta,
        Column('id', Integer, primary_key=True),
        Column('address', String, nullable=False)
    )

    customer = Table(
        'customer', meta,
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False)
    )

    device = Table(
        'device', meta,
        Column('id', Integer, primary_key=True),
        Column('device_type', String, nullable=False),
        Column('facility', Integer, ForeignKey("facility.id"), nullable=False),
        Column('location_description', String)
    )

    data = Table(
        'data', meta,
        Column('id', Integer, primary_key=True),
        Column('timestamp', DateTime, default=datetime.datetime.utcnow),
        Column('device', Integer, ForeignKey("device.id"), nullable=False),
        Column('t1', Float),
        Column('t2', Float),
        Column('t3', Float),
        Column('power', Float),
        Column('operation', String(4), nullable=False),
        Column('fan_on', Boolean, nullable=False)
    )

con, meta = connect('catalog', 'catalog', 'acmonitor')
print(con, meta)

setup()
meta.create_all(con)
