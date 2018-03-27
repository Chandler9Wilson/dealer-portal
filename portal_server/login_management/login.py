import json

# flask-login used for login management and persistence
from flask_login import login_required, login_user, logout_user

# used for google oauth verification of tokens
from google.oauth2 import id_token
from google.auth.transport import requests as googleRequests

from flask import Blueprint, render_template, request, redirect, url_for

# Import database classes and SQLAlchamy instance
from portal_server.db.models import User, db

login_bp = Blueprint('login_bp', __name__,
                     static_folder='login_static',
                     template_folder='templates')


@login_bp.route('/login/')
def login():
    # flask_login.logout_user()
    return render_template('login.html')


@login_bp.route('/logout/')
def logout():
    logout_user()

    return redirect(url_for('login_bp.login'))


@login_bp.route('/debug/')
def debug():

    return infoMessage


# Begin POST only views mainly used for login


@login_bp.route('/gconnect/', methods=['POST'])
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
        if idinfo['iss'] not in ['accounts.google.com',
                                 'https://accounts.google.com']:
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
                return redirect(url_for('directory.home'))
    except ValueError:
        # TODO change to feed an error back to the user

        # Invalid token
        return render_template('login.html')

    return render_template('directory.html')
