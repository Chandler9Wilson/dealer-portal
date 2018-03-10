# TODO this needs better names
def get_items_related(owner, owned_name, owned_class, obj):
    # Retrieves up to the first 500 items of db_class \
    # with a relationship with owned name and
    # returns as a dictionary or object list depending on obj

    # TODO evaluate if this needs a limit or not
    item_list = getattr(owner, owned_name)
    # Really a list of dictionaries but couldn't think of a better name
    item_dicts = []

    for item in item_list:
        item_dicts.append(owned_class.as_dict(item))

    # TODO Might want to move jsonify to the view function?
    return jsonify(item_dicts)


def create_item(db_class, request_json):
    # Creates a db entry with data from request_json,
    # schema from columns and db_class

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
    # loop through an item and update any valid changes

    for attribute, value in request_json.items():
        if attribute in db_class.required_columns() and value is not None:
            setattr(item, attribute, value)
        elif attribute in db_class.available_columns():
            setattr(item, attribute, value)

    # TODO add a try catch for sqlalchemy errors
    db.session.commit()

    return item


@app.route('/customers/', methods=['POST'])
def create_customer():
    # Create a new customer

    if request.get_json() is None:
        # This is triggered if the mimetype is not application/json
        return abort(415)
    # If get_json() decoding fails it will call \
    # http://flask.pocoo.org/docs/0.12/api/#flask.Request.on_json_loading_failed
    raw_customer = request.get_json()

    # create_item() handles class creation and db commit
    instance = create_item(Customer, raw_customer)

    try:
        return jsonify(instance.as_dict())
    except:
        # TODO pass more helpfull messages
        abort(400)
        raise


@app.route('/customers/<int:customer_id>/', methods=['GET'])
def get_customer(customer_id):
    # Get a specific customer by id

    customer = Customer.query.filter_by(id=customer_id).first()

    if customer is None:
        return abort(404)
    else:
        return jsonify(Customer.as_dict(customer))


@app.route('/customers/<int:customer_id>/', methods=['PUT'])
def update_customer(customer_id):
    # Update a customer by id
    # Currently does not accept non existant customers (no new)

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

    # TODO add a more descriptive message
    # TODO add a 201 status code to request
    try:
        return jsonify(updated_customer.as_dict())
    except:
        abort(400)
        raise


@app.route('/customers/<int:customer_id>/', methods=['DELETE'])
def delete_customer(customer_id):
    # Delete a specific customer by id

    customer = Customer.query.filter_by(id=customer_id).first()

    if customer is None:
        return abort(404)
    else:
        db.session.delete(customer)

        # TODO add a try catch for sqlalchemy errors
        db.session.commit()

        return 'Deleted the customer'


@app.route('/customers/<int:customer_id>/facilities/', methods=['GET'])
def facilities_of_customer(customer_id):
    # Get facilities with a foreign key of customer_id

    customer = Customer.query.filter_by(id=customer_id).first()

    facilities_list = get_items_of(customer, 'facilities', Facility)

    return facilities_list


@app.route('/customers/<int:customer_id>/facilities/devices',
           methods=['GET'])
def devices_of_customers_facility(customer_id):
    # Get facilities with a foreign key of customer_id

    customer = Customer.query.filter_by(id=customer_id).first()

    facilities_list = get_items_of(customer, 'facilities', Facility)

    return facilities_list


@app.route('/facilities/', methods=['GET'])
def get_facilities():
    # GET a list of up to the first 20 facilities
    facility_json = get_items(Facility)

    return facility_json


@app.route('/facilities/', methods=['POST'])
def create_facility():
    # Create a new facility

    if request.get_json() is None:
        # This is triggered if the mimetype is not application/json
        return abort(415)
    # If get_json() decoding fails it will call \
    # http://flask.pocoo.org/docs/0.12/api/#flask.Request.on_json_loading_failed
    raw_facility = request.get_json()

    # create_item() handles class creation and db commit
    instance = create_item(Facility, raw_facility)

    try:
        facility_address = instance.address
        # TODO create custom handler for api success
        return 'Facility created with address %s' % (facility_address)
    except:
        # TODO pass more helpfull messages
        abort(400)
        raise


@app.route('/facilities/<int:facility_id>/', methods=['GET'])
def get_facility(facility_id):
    # Get a specific facility by id

    facility = Facility.query.filter_by(id=facility_id).first()

    if facility is None:
        return abort(404)
    else:
        return jsonify(Facility.as_dict(facility))


@app.route('/facilities/<int:facility_id>/', methods=['PUT'])
def update_facility(facility_id):
    # Update a facility by id
    # Currently does not accept non existant facilities (no new)

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

    # TODO add a more descriptive message
    # TODO add a 201 status code to request
    try:
        return jsonify(updated_facility.as_dict())
    except:
        abort(400)
        raise


@app.route('/facilities/<int:facility_id>/', methods=['DELETE'])
def delete_facility(facility_id):
    # Delete a specific facility by id

    facility = Facility.query.filter_by(id=facility_id).first()

    if facility is None:
        return abort(404)
    else:
        db.session.delete(facility)

        # TODO add a try catch for sqlalchemy errors
        db.session.commit()

        return 'Deleted the facility'


@app.route('/devices/', methods=['GET'])
def get_devices():
    # GET a list of up to the first 20 devices
    device_json = get_items(Device)

    return device_json


@app.route('/devices/', methods=['POST'])
def create_device():
    # Create a new device

    if request.get_json() is None:
        # This is triggered if the mimetype is not application/json
        return abort(415)
    # If get_json() decoding fails it will call \
    # http://flask.pocoo.org/docs/0.12/api/#flask.Request.on_json_loading_failed
    raw_device = request.get_json()

    # create_item() handles class creation and db commit
    instance = create_item(Device, raw_device)

    try:
        device_id = instance.hardware_id
        # TODO create custom handler for api success
        return 'Device created with hardware id %s' % (device_id)
    except:
        # TODO pass more helpfull messages
        abort(400)
        raise


@app.route('/devices/<int:device_id>/', methods=['GET'])
def get_device(device_id):
    # Get a specific device by id

    device = Device.query.filter_by(id=device_id).first()

    if device is None:
        return abort(404)
    else:
        return jsonify(Device.as_dict(device))


@app.route('/devices/<int:device_id>/', methods=['PUT'])
def update_device(device_id):
    # Update a device by id
    # Currently does not accept non existant devices (no new)

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

    # TODO add a more descriptive message
    # TODO add a 201 status code to request
    try:
        return jsonify(updated_device.as_dict())
    except:
        abort(400)
        raise


@app.route('/devices/<int:device_id>/', methods=['DELETE'])
def delete_device(device_id):
    # Delete a specific device by id

    device = Device.query.filter_by(id=device_id).first()

    if device is None:
        return abort(404)
    else:
        db.session.delete(device)

        # TODO add a try catch for sqlalchemy errors
        db.session.commit()

        return 'Deleted the device'


@app.route('/data/', methods=['POST'])
def new_data():
    # Takes a data json and adds to db

    if request.get_json() is None:
        # This is triggered if the mimetype is not application/json
        return abort(415)
    # If get_json() decoding fails it will call \
    # http://flask.pocoo.org/docs/0.12/api/#flask.Request.on_json_loading_failed
    raw_data = request.get_json()

    # create_item() handles class creation and db commit
    instance = create_item(Data, raw_data)

    try:
        return jsonify(instance.as_dict())
    except:
        # TODO pass more helpfull messages
        abort(400)
        raise
