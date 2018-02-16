import random
import string
import json
import os
import time

from flask import Flask, session, render_template, request, url_for, flash, \
    redirect, Response, make_response, jsonify, abort

# flask-login used for login management and persistence
from flask_login import LoginManager, login_user, login_required, current_user

# Import database classes and SQLAlchamy instance
from db.models import Customer, Facility, Device, \
    Data, User, UserToFacility, Role, db

# used for google oauth verification of tokens
from google.oauth2 import id_token
from google.auth.transport import requests as googleRequests

# makes sure this is different from other files flask(__name__) or
# some storage is shared
app = Flask(__name__)

# TODO make config options more succinct
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://catalog:catalog@' + \
    'localhost:5432/acmonitor'
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

# Flask-Login class
login_manager = LoginManager()
# login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    u = User.query.filter_by(id=id).first()
    # TODO investigate if im just creating duplicates here?
    return User(u.email, u.oauth_provider)


'''
@login_manager.unauthorized_handler
def handler_needs_login():
    flash("You have to be logged in to access this page.")
    return redirect(url_for('account.login', next=request.endpoint))


def redirect_dest(fallback):
    dest = request.args.get('next')
    try:
        dest_url = url_for(dest)
    except:
        return redirect(fallback)
    return redirect(dest_url) '''


@app.route('/login/')
def login():
    # flask_login.logout_user()
    return render_template('login.html')


@app.route('/home/')
@login_required
def home():
    return render_template('directory.html')


@app.route('/debug/')
def debug():

    return infoMessage


# Begin POST only views mainly used for login


@app.route('/gconnect/', methods=['POST'])
def gconnect():
    # Handles google login requests
    CLIENT_ID = '349469004723-j9csi1hlhb1s0abuap24lo50mgvbkrhh' + \
        '.apps.googleusercontent.com'
    tokenJSON = json.loads(request.data.decode('utf-8'))

    try:
        token = tokenJSON['idtoken']

        # Google library verifies the JWT signature (signed JSON Web Token)
        # and the audience and expiration claim
        idinfo = id_token.verify_oauth2_token(
            token, googleRequests.Request(), CLIENT_ID)

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        # Checks if issuer of the token is google
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        else:
            # Check if user is in the DB
            user_email = idinfo['email']
            user = User.query.filter_by(email=user_email).first()

            if user:
                login_user(user, True)

                # TODO return something usefull
                return 'Hello World'
            else:
                # TODO improve adding a new user info attached to idinfo obj
                new_user = User(email=user_email, oauth_provider='google')
                db.session.add(new_user)
                try:
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(str(e))
                    return "An error occured"
                return redirect(url_for('home'))
    except ValueError:
        # TODO change to feed an error back to the user

        # Invalid token
        return render_template('login.html')

    return render_template('directory.html')


# Begin API views and functions


def get_items(db_class):
    # Retrieves up to the first 20 items of a db_class defined in models

    item_list = db_class.query.limit(20).all()
    # Really a list of dictionaries but couldn't think of a better name
    item_dicts = []

    for item in item_list:
        item_dicts.append(db_class.as_dict(item))

    # Might want to move jsonify to the view function?
    return jsonify(item_dicts)


def create_item(db_class, request_json, required_columns):
    # Creates a db entry with data from request_json,
    # schema from columns and db_class

    item_columns = {}

    try:
        for column in required_columns:
            item_columns[column] = request_json[column]
    except KeyError as e:
        error_message = 'KeyError - reason %s was not found' % str(e)
        return jsonify(error_message)
    except:
        abort(400)
        raise
    else:
        new_item = db_class.from_dict(item_columns)
        db.session.add(new_item)

        # TODO add a try catch for sqlalchemy errors
        db.session.commit()

    # TODO add a more descriptive message
    # TODO add a 201 status code to request
    return new_item


def update_item(db_class, item, request_json):
    # loop through an item and update any valid changes

    for attribute, value in request_json.items():
        if attribute in item.required_columns() and value is not None:
            setattr(item, attribute, value)
        elif attribute in item.available_columns():
            setattr(item, attribute, value)

    # TODO add a try catch for sqlalchemy errors
    db.session.commit()

    return item


@app.route('/api/customers/', methods=['GET'])
def get_customers():
    # GET a list of up to the first 20 customers
    customer_json = get_items(Customer)

    return customer_json


@app.route('/api/customers/', methods=['POST'])
def create_customer():
    # Create a new customer

    required_columns = ['name']

    if request.get_json() is None:
        # This is triggered if the mimetype is not application/json
        return abort(415)
    # If get_json() decoding fails it will call \
    # http://flask.pocoo.org/docs/0.12/api/#flask.Request.on_json_loading_failed
    raw_customer = request.get_json()

    # create_item() handles class creation and db commit
    instance = create_item(Customer, raw_customer, required_columns)

    try:
        customer_name = instance.name
        # TODO create custom handler for api success
        return 'Customer created with name %s' % (customer_name)
    except:
        # TODO pass more helpfull messages
        abort(400)
        raise


@app.route('/api/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    # Get a specific customer by id

    customer = Customer.query.filter_by(id=customer_id).first()

    if customer is None:
        return abort(404)
    else:
        return jsonify(Customer.as_dict(customer))


@app.route('/api/customers/<int:customer_id>', methods=['PUT'])
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


@app.route('/api/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    # Get a specific customer by id

    customer = Customer.query.filter_by(id=customer_id).first()

    if customer is None:
        return abort(404)
    else:
        db.session.delete(customer)

        # TODO add a try catch for sqlalchemy errors
        db.session.commit()

        return 'Deleted the customer'


@app.route('/api/facilities/', methods=['GET'])
def get_facilities():
    # GET a list of up to the first 20 facilities
    facility_json = get_items(Facility)

    return facility_json


@app.route('/api/facilities/', methods=['POST'])
def create_facility():
    # Create a new facility

    required_columns = ['address']

    if request.get_json() is None:
        # This is triggered if the mimetype is not application/json
        return abort(415)
    # If get_json() decoding fails it will call \
    # http://flask.pocoo.org/docs/0.12/api/#flask.Request.on_json_loading_failed
    raw_facility = request.get_json()

    # create_item() handles class creation and db commit
    instance = create_item(Facility, raw_facility, required_columns)

    try:
        facility_address = instance.address
        # TODO create custom handler for api success
        return 'Facility created with address %s' % (facility_address)
    except:
        # TODO pass more helpfull messages
        abort(400)
        raise


@app.route('/api/facilities/<int:facility_id>', methods=['GET'])
def get_facility(facility_id):
    # Get a specific facility by id

    facility = Facility.query.filter_by(id=facility_id).first()

    if facility is None:
        return abort(404)
    else:
        return jsonify(Facility.as_dict(facility))


@app.route('/api/facilities/<int:facility_id>', methods=['PUT'])
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


@app.route('/api/devices/', methods=['GET'])
def get_devices():
    # GET a list of up to the first 20 devices
    device_json = get_items(Device)

    return device_json


@app.route('/api/devices/', methods=['POST'])
def create_device():
    # Create a new device

    required_columns = ['device_type', 'hardware_id']

    if request.get_json() is None:
        # This is triggered if the mimetype is not application/json
        return abort(415)
    # If get_json() decoding fails it will call \
    # http://flask.pocoo.org/docs/0.12/api/#flask.Request.on_json_loading_failed
    raw_device = request.get_json()

    # create_item() handles class creation and db commit
    instance = create_item(Device, raw_device, required_columns)

    try:
        device_id = instance.hardware_id
        # TODO create custom handler for api success
        return 'Device created with hardware id %s' % (device_id)
    except:
        # TODO pass more helpfull messages
        abort(400)
        raise


@app.route('/api/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    # Get a specific device by id

    device = Device.query.filter_by(id=device_id).first()

    if device is None:
        return abort(404)
    else:
        return jsonify(Device.as_dict(device))


@app.route('/api/devices/<int:device_id>', methods=['PUT'])
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


# TODO this needs a better name
# Begin flask modifications


# TODO customer messages https://stackoverflow.com/a/21301229/6879253
@app.errorhandler(400)
def not_found(error):
    # Handle 400 errors so that they make more sense for the api
    # TODO make this error a bit more descriptive

    return make_response(jsonify({'error': 'Failed to decode'}), 400)


@app.errorhandler(404)
def not_found(error):
    # Handle 404 errors so that they make more sense for the api
    # TODO make this error a bit more descriptive

    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(415)
def not_found(error):
    # Handle 415 errors so that they make more sense for the api
    # TODO make this error a bit more descriptive

    return make_response(
        jsonify({'error': 'You sent an unsupported media type'}), 415)


@app.context_processor
# TODO remove before deployment
def override_url_for():
    # overides static file caching
    """
    Generate a new token on every request to prevent the browser from
    caching static files.
    """
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == '__main__':
    # TODO change secret_key
    app.secret_key = 'super secret key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000, threaded=True)
