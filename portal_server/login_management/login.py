import json

# flask-login used for login management and persistence
from flask_login import login_required, login_user, logout_user

# flask-principal is used for per resource control and permissions
from flask_principal import Identity, AnonymousIdentity, identity_changed

# used for google oauth verification of tokens
from google.oauth2 import id_token
from google.auth.transport import requests as googleRequests

from flask import Blueprint, render_template, request, redirect, url_for, \
    current_app, session, make_response

# Import database classes and SQLAlchamy instance
from portal_server.db.models import User, Role, db

login_bp = Blueprint('login_bp', __name__,
                     static_folder='login_static',
                     template_folder='templates')


def google_verify(tokenJSON):
    """Given a Google JWT attempts to verify using google libraries"""
    CLIENT_ID = '349469004723-j9csi1hlhb1s0abuap24lo50mgvbkrhh' + \
        '.apps.googleusercontent.com'
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
    if idinfo['iss'] not in ['accounts.google.com',
                             'https://accounts.google.com']:
        raise ValueError('Wrong issuer.')
    else:
        return idinfo


def create_user(user_dict, stage=None):
    """A simple wrapper around ``User.from_dict()`` with db commit logic

    Args:
        user_dict (dict): A dictionary containing all necessary ``User``
            paramaters.
        stage (bool): A control on whether the new_user is commited to
            the db or kept in the session. This is useful for when you
            would like to link data before a commit.

    Returns:
        new_user (obj): A new ``User`` instance object
    """
    new_user = User.from_dict(user_dict)
    db.session.add(new_user)

    if stage:
        return new_user
    else:
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise
        else:
            return new_user


def create_admin(user_dict):
    """Creates a new ``User`` and a linked admin ``Role``"""
    new_user = create_user(user_dict, 'stage')

    new_role = Role(title='admin')
    new_role.user = new_user

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise
    else:
        return new_user


def complete_login(user):
    """Given a user, logs in said user and sets the user's role

    Args:
        user (obj): A valid ``User`` instance object

    Returns:
        bool: Returns true on success should throw exception otherwise.
    """
    # Keep the user info in the session using Flask-Login
    login_user(user, True)

    # Tell Flask-Principal the identity changed
    identity_changed.send(current_app._get_current_object(),
                          identity=Identity(user.id))

    return True


def first_user():
    """A check on whether or not there are users in the ``User`` table

    Returns:
        bool: Returns True if there are no users in the table, False otherwise.
    """
    user = User.query.first()

    if user:
        return False
    else:
        return True


@login_bp.route('/login/')
def login():
    # flask_login.logout_user()
    return render_template('login.html')


@login_bp.route('/logout/')
def logout():
    # Remove the user information from the session
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())

    return redirect(url_for('login_bp.login'))


@login_bp.route('/debug/')
def debug():
    return redirect(url_for('login_bp.login'))

# Begin POST only views mainly used for login


@login_bp.route('/gconnect/', methods=['POST'])
def gconnect():
    """Handles Google identity login requests"""
    tokenJSON = json.loads(request.data.decode('utf-8'))

    try:
        idinfo = google_verify(tokenJSON)

        # Check if user is in the DB
        user_email = idinfo['email']
        user = User.query.filter_by(email=user_email).first()

        if user:
            complete_login(user)

            return make_response('Logged in succesfully', 200)
        elif first_user():
            user_info = {
                'email': user_email,
                'oauth_provider': 'google',
                'name': idinfo.get('name'),
                'profile_pic': idinfo.get('picture')
            }

            new_admin = create_admin(user_info)

            # login so redirects works
            complete_login(new_admin)

            return make_response('Created admin succesfully', 200)
        else:
            return make_response(jsonify({'error': 'Contact the server ' +
                                          'admin for login privilages'}), 401)
    except ValueError:

        # Invalid token
        return make_response(jsonify({'error': 'Invalid Token'}), 401)
