# This needs to be run as python -m portal_server.db.import_fake_data
# from the project root with an activated venv
import json
import sys

from portal_server import app

# Import database classes and SQLAlchamy instance
from portal_server.db.models import Customer, Facility, Device, \
    Data, Role, db


def create_item(db_class, request_json):
    """Creates a db entry and commits it

    Schema is pulled from an imported db_class
    """

    required_columns = db_class.required_columns()

    try:
        # TODO change to a list comprehension
        for column in required_columns:
            required_attribute = request_json.get(column)

            if required_attribute is not None:
                continue
            elif required_attribute is None:
                raise ValueError('A required attribute had a value of None')
    except KeyError as e:
        error_message = 'KeyError - reason %s was not found' % str(e)
        print(error_message, '32')
    else:
        new_item = db_class.from_dict(request_json)

        with app.app_context():
            db.session.add(new_item)

            db.session.commit()

    return new_item


def stage_item(db_class, request_json):
    """ Creates a db entry with data from request_json

    This does not commit to the db, you will need to call
    `db.commit(your_item)`. The schema is pulled from db_class.
    """
    required_columns = db_class.required_columns()

    try:
        # TODO change to a list comprehension
        for column in required_columns:
            required_attribute = request_json.get(column)

            if required_attribute:
                continue
            else:
                print(column, '60')
                raise ValueError('A required attribute evaluated to false')
    except KeyError as e:
        error_message = 'KeyError - reason %s was not found' % str(e)
        print(error_message, '64')
    else:
        new_item = db_class.from_dict(request_json)

    return new_item


def parse_data(data):

    customers = data.get('customers')
    facilities = data.get('facilities')
    devices = data.get('devices')
    data_points = data.get('data_points')
    sets = data.get('sets')

    if customers:
        for customer in customers:
            create_item(Customer, customer)

    if facilities:
        for facility in facilities:
            create_item(Facility, facility)

    if devices:
        for device in devices:
            create_item(Device, device)

    if data_points:
        for point in data_points:
            create_item(Data, point)

    if sets:
        for obj in sets:

            with app.app_context():
                customer = stage_item(Customer, obj['customer'])
                db.session.add(customer)

                for facility in obj['facilities']:
                    new_facility = stage_item(Facility, facility)
                    db.session.add(new_facility)

                    new_facility.customer = customer

                    for device in obj['devices']:
                        if device['address'] == new_facility.address:
                            new_device = stage_item(Device, device)
                            db.session.add(new_device)

                            new_device.facility = new_facility

                            data_points = device.get('data_points')

                            if data_points:
                                for data_point in data_points:
                                    new_data = stage_item(Data, data_point)
                                    db.session.add(new_data)

                                    new_data.device = new_device
                        else:
                            continue

                # TODO add a try catch for sqlalchemy errors
                db.session.commit()


def load_data():
    """This returns a decoded json

    Feel free to change the path to a different data set it defaults
    to a small one.
    """
    path_to_json = 'portal_server/db/fake_data.JSON'

    # good explenation of with http://effbot.org/zone/python-with-statement.htm
    with open(path_to_json) as fake_data:
        data = json.load(fake_data)

    return data


if __name__ == '__main__':
    parse_data(load_data())
