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


# Begin API views


@app.route('/api/customers/', methods=['GET'])
def get_customers():
    # GET a list of up to the first 20 customers

    customer_list = Customer.query.limit(20).all()
    customer_dict = []

    for customer in customer_list:
        customer_dict.append(Customer.as_dict(customer))

    return jsonify(customer_dict)


@app.route('/api/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    # Get a specific customer by id

    customer = Customer.query.filter_by(id=customer_id).first()

    if customer is None:
        return abort(404)
    else:
        return jsonify(Customer.as_dict(customer))


@app.route('/api/facilities', methods=['GET'])
def get_facilities():
    # GET a list of up to the first 20 facilities

    facility_list = Facility.query.limit(20).all()
    facility_dict = []

    for facility in facility_list:
        facility_dict.append(Facility.as_dict(facility))

    return jsonify(facility_dict)


@app.route('/api/facilities/<int:facility_id>', methods=['GET'])
def get_facility(facility_id):
    # Get a specific facility by id

    facility = Facility.query.filter_by(id=facility_id).first()

    if facility is None:
        return abort(404)
    else:
        return jsonify(Facility.as_dict(facility))


@app.route('/api/devices', methods=['GET'])
def get_devices():
    # GET a list of up to the first 20 devices

    device_list = Device.query.limit(20).all()
    device_dict = []

    for device in device_list:
        device_dict.append(Device.as_dict(device))

    return jsonify(device_dict)


@app.route('/api/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    # Get a specific device by id

    device = Device.query.filter_by(id=device_id).first()

    if device is None:
        return abort(404)
    else:
        return jsonify(Device.as_dict(device))


@app.errorhandler(404)
def not_found(error):
    # handle 404 errors so that they make more sense for the api
    # TODO make this error a bit more descriptive

    return make_response(jsonify({'error': 'Not found'}), 404)


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
