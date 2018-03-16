from flask import Blueprint, jsonify, abort, make_response, request

from portal_server.db.models import Customer, Facility, Device, Data, db

api = Blueprint('api', __name__)


def get_items(db_class):
    """Retrieves up to the first 500 items of a db_class defined in models"""
    item_list = db_class.query.limit(500).all()
    # Really a list of dictionaries but couldn't think of a better name
    item_dicts = []

    for item in item_list:
        item_dicts.append(db_class.as_dict(item))

    # TODO Might want to move jsonify to the view function?
    return jsonify(item_dicts)


def create_item(db_class, request_json):
    """Creates a db entry

    with data from request_json,
    schema from columns and db_class"""
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
        return jsonify(error_message)
    except:
        abort(400)
        raise
    else:
        new_item = db_class.from_dict(request_json)
        db.session.add(new_item)

        # TODO add a try catch for sqlalchemy errors
        db.session.commit()

    # TODO add a more descriptive message
    # TODO add a 201 status code to request
    return new_item


def update_item(db_class, item, request_json):
    """loop through an item and update any valid changes"""
    for attribute, value in request_json.items():
        if attribute in db_class.required_columns() and value is not None:
            setattr(item, attribute, value)
        elif attribute in db_class.available_columns():
            setattr(item, attribute, value)

    # TODO add a try catch for sqlalchemy errors
    db.session.commit()

    return item


@api.route('/customers/', methods=['POST'])
def create_customer():
    """Create a new customer"""
    if request.get_json() is None:
        # This is triggered if the mimetype is not application/json
        return abort(415)
    # If get_json() decoding fails it will call \
    # http://flask.pocoo.org/docs/0.12/api/#flask.Request.on_json_loading_failed
    raw_customer = request.get_json()

    # create_item() handles class creation and db commit
    instance = create_item(Customer, raw_customer)

    return make_response(jsonify(instance.as_dict()), 201)


@api.route('/customers/<int:customer_id>/', methods=['PUT'])
def update_customer(customer_id):
    """Update a customer

    Currently does not accept non existant customers (no new)"""
    customer = Customer.query.filter_by(id=customer_id).first()

    if customer is None:
        return abort(404)
    if request.get_json() is None:
        # This is triggered if the mimetype is not application/json
        return abort(415)

    # If get_json() decoding fails it will call \
    # http://flask.pocoo.org/docs/0.12/api/#flask.Request.on_json_loading_failed
    raw_update = request.get_json()

    updated_customer = update_item(Customer, customer, raw_update)

    return make_response(jsonify(updated_customer.as_dict()), 200)


@api.route('/customers/<int:customer_id>/', methods=['DELETE'])
def delete_customer(customer_id):
    """Delete a specific customer by id"""

    customer = Customer.query.filter_by(id=customer_id).first()

    if customer is None:
        return abort(404)
    else:
        db.session.delete(customer)

        # TODO add a try catch for sqlalchemy errors
        db.session.commit()

        return make_response('', 204)


@api.route('/customers/', methods=['GET'])
@api.route('/customers/<int:customer_id>/', methods=['GET'])
def get_customers(customer_id=None):
    """Returns a customer or customers"""
    if customer_id is None:
        customer_json = get_items(Customer)
    else:
        customer = Customer.query.filter_by(id=customer_id).first()

        if customer is None:
            return abort(404)
        else:
            customer_json = jsonify(Customer.as_dict(customer))

    return customer_json


@api.route('/customers/<int:customer_id>/facilities/', methods=['GET'])
def facilities_of_customer(customer_id):
    """Returns facilities with a relationship to customer_id"""
    customer = Customer.query.filter_by(id=customer_id).first()

    if customer is None:
        return abort(404)
    else:
        facility_list = customer.facilities
        facility_dicts = []

        for facility in facility_list:
            facility_dicts.append(facility.as_dict())
        return jsonify(facility_dicts)


@api.route('/customers/<int:customer_id>/devices/', methods=['GET'])
def devices_of_customer(customer_id):
    """Returns devices with a relationship to customer_id"""
    customer = Customer.query.filter_by(id=customer_id).first()

    if customer is None:
        return abort(404)
    else:
        facility_list = customer.facilities
        device_dicts = []

        for facility in facility_list:
            for device in facility.devices:
                device_dicts.append(device.as_dict())
                print(device_dicts)
    return jsonify(device_dicts)


@api.route('/customers/<int:customer_id>/facilities/devices/', methods=['GET'])
# TODO come up with a less verbose name
def devices_of_facilities_of_customer(customer_id):
    """Returns facilities with nested devices owned by customer_id"""
    customer = Customer.query.filter_by(id=customer_id).first()

    if customer is None:
        return abort(404)
    else:
        # TODO look into adding this logic to a method on Facility
        facility_list = customer.facilities
        # TODO come up with a better name
        nested_dicts = []

        for index, facility in enumerate(facility_list):
            nested_dicts.append(facility.as_dict())
            # Adds an empty list to current facility
            nested_dicts[index]['devices'] = []
            devices = nested_dicts[index]['devices']

            for device in facility.devices:
                devices.append(device.as_dict())
    return jsonify(nested_dicts)


@api.route('/facilities/', methods=['POST'])
def create_facility():
    """Create a new facility"""
    if request.get_json() is None:
        # This is triggered if the mimetype is not application/json
        return abort(415)
    # If get_json() decoding fails it will call \
    # http://flask.pocoo.org/docs/0.12/api/#flask.Request.on_json_loading_failed
    raw_facility = request.get_json()

    # create_item() handles class creation and db commit
    instance = create_item(Facility, raw_facility)

    return make_response(jsonify(instance.as_dict()), 201)


@api.route('/facilities/<int:facility_id>/', methods=['PUT'])
def update_facility(facility_id):
    """Update a facility by id

    Currently does not accept non existant facilities (no new)"""
    facility = Facility.query.filter_by(id=facility_id).first()

    if facility is None:
        return abort(404)
    if request.get_json() is None:
        # This is triggered if the mimetype is not application/json
        return abort(415)

    # If get_json() decoding fails it will call \
    # http://flask.pocoo.org/docs/0.12/api/#flask.Request.on_json_loading_failed
    raw_update = request.get_json()

    updated_facility = update_item(Facility, facility, raw_update)

    return make_response(jsonify(updated_facility.as_dict()), 200)


@api.route('/facilities/<int:facility_id>/', methods=['DELETE'])
def delete_facility(facility_id):
    """Delete a specific facility by id"""
    facility = Facility.query.filter_by(id=facility_id).first()

    if facility is None:
        return abort(404)
    else:
        db.session.delete(facility)

        # TODO add a try catch for sqlalchemy errors
        db.session.commit()

        return make_response('', 204)


@api.route('/facilities/', methods=['GET'])
@api.route('/facilities/<int:facility_id>/', methods=['GET'])
def get_facilities(facility_id=None):
    """Returns a facility or facilities"""
    if facility_id is None:
        facility_json = get_items(Facility)
    else:
        facility = Facility.query.filter_by(id=facility_id).first()

        if facility is None:
            return abort(404)
        else:
            facility_json = jsonify(Facility.as_dict(facility))

    return facility_json


@api.route('/facilities/<int:facility_id>/devices/', methods=['GET'])
def devices_of_facility(facility_id):
    """Returns devices with a relationship to facility_id"""
    facility = Facility.query.filter_by(id=facility_id).first()

    if facility is None:
        return abort(404)
    else:
        device_list = facility.devices
        device_dicts = []

        for device in device_list:
            device_dicts.append(device.as_dict())

    return jsonify(device_dicts)


@api.route('/facilities/<int:facility_id>/devices/data/', methods=['GET'])
def data_of_facility(facility_id):
    """Returns devices with nested data owned by facility_id"""
    facility = Facility.query.filter_by(id=facility_id).first()

    if facility is None:
        return abort(404)
    else:
        device_list = facility.devices
        # TODO come up with a better name
        nested_dicts = []

        for index, device in enumerate(device_list):
            nested_dicts.append(device.as_dict())
            # Adds an empty list to current facility
            nested_dicts[index]['data'] = []
            data = nested_dicts[index]['data']

            for data in device.data:
                data.append(data.as_dict())

    return jsonify(nested_dicts)


@api.route('/devices/', methods=['POST'])
def create_device():
    """Create a new device"""
    if request.get_json() is None:
        # This is triggered if the mimetype is not application/json
        return abort(415)
    # If get_json() decoding fails it will call \
    # http://flask.pocoo.org/docs/0.12/api/#flask.Request.on_json_loading_failed
    raw_device = request.get_json()

    # create_item() handles class creation and db commit
    instance = create_item(Device, raw_device)

    return make_response(jsonify(instance.as_dict()), 201)


@api.route('/devices/<int:device_id>/', methods=['PUT'])
def update_device(device_id):
    """Update a device by id

    Currently does not accept non existant devices (no new)"""
    device = Device.query.filter_by(id=device_id).first()

    if device is None:
        return abort(404)
    if request.get_json() is None:
        # This is triggered if the mimetype is not application/json
        return abort(415)

    # If get_json() decoding fails it will call \
    # http://flask.pocoo.org/docs/0.12/api/#flask.Request.on_json_loading_failed
    raw_update = request.get_json()

    updated_device = update_item(Device, device, raw_update)

    return make_response(jsonify(updated_device.as_dict()), 200)


@api.route('/devices/<int:device_id>/', methods=['DELETE'])
def delete_device(device_id):
    """Delete a specific device by id"""
    device = Device.query.filter_by(id=device_id).first()

    if device is None:
        return abort(404)
    else:
        db.session.delete(device)

        # TODO add a try catch for sqlalchemy errors
        db.session.commit()

        return make_response('', 204)


@api.route('/devices/', methods=['GET'])
@api.route('/devices/<int:device_id>/', methods=['GET'])
def get_devices(device_id=None):

    if device_id is None:
        device_json = get_items(Device)
    else:
        device = Device.query.filter_by(id=device_id).first()

        if device is None:
            return abort(404)
        else:
            device_json = jsonify(Device.as_dict(device))

    return device_json


@api.route('/devices/<int:device_id>/data/', methods=['GET'])
def data_of_device(device_id):
    """Returns devices with a relationship to device_id"""
    device = Device.query.filter_by(id=device_id).first()

    if device is None:
        return abort(404)
    else:
        data_list = device.data
        data_dicts = []

        for data in data_list:
            data_dicts.append(data.as_dict())

    return jsonify(data_dicts)


@api.route('/data/', methods=['POST'])
def new_data():
    """Takes a data json and adds to db"""
    if request.get_json() is None:
        # This is triggered if the mimetype is not application/json
        return abort(415)
    # If get_json() decoding fails it will call \
    # http://flask.pocoo.org/docs/0.12/api/#flask.Request.on_json_loading_failed
    raw_data = request.get_json()

    # create_item() handles class creation and db commit
    instance = create_item(Data, raw_data)

    return make_response(jsonify(instance.as_dict()), 201)


# TODO custom messages https://stackoverflow.com/a/21301229/6879253


@api.errorhandler(400)
def failed_decode(error):
    # Handle 400 errors so that they make more sense for the api
    # TODO make this error a bit more descriptive

    return make_response(jsonify({'error': 'Failed to decode'}), 400)


@api.errorhandler(404)
def not_found(error):
    # Handle 404 errors so that they make more sense for the api
    # TODO make this error a bit more descriptive

    return make_response(jsonify({'error': 'Not found'}), 404)


@api.errorhandler(415)
def unsupported(error):
    # Handle 415 errors so that they make more sense for the api
    # TODO make this error a bit more descriptive

    return make_response(
        jsonify({'error': 'You sent an unsupported media type'}), 415)


@api.errorhandler(500)
def internal_error(error):
    # Handle 500 errors so that they make more sense for the api
    # This will not work properly when debug=true
    # TODO make this error a bit more descriptive

    return make_response(jsonify({'error': 'Internal server error'}), 500)
