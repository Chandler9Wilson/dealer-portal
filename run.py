import random
import string
import json
import os

from flask import Flask, session, render_template, request, url_for

# used for google oauth verification of tokens
from google.oauth2 import id_token
from google.auth.transport import requests as googleRequests

# makes sure this is different from the main files flask name or cookies
# etc will be shared
app = Flask(__name__)


@app.route('/login')
def login():
    print '-' * 30
    print request.headers
    print '-' * 30
    print session

    return render_template('login.html')


@app.route('/home')
def home():

    return render_template('directory.html')


@app.route('/debug')
def debug():
    # TODO remove for production
    print session

    return infoMessage


@app.route('/gconnect', methods=['POST'])
def gconnect():

    CLIENT_ID = '349469004723-j9csi1hlhb1s0abuap24lo50mgvbkrhh' + \
        '.apps.googleusercontent.com'
    tokenJSON = json.loads(request.data)

    print '-' * 30
    print 'gconnect called'
    print '-' * 30
    print request.headers

    try:
        token = tokenJSON['idtoken']

        idinfo = id_token.verify_oauth2_token(
            token, googleRequests.Request(), CLIENT_ID)

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        # ID token is valid. Get the user's Google Account ID from the decoded
        # token.
        userid = idinfo['sub']
    except ValueError:
        # TODO change to feed an error back to the user

        # Invalid token
        return render_template('login.html')

    return render_template('directory.html')


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
    app.run(host='0.0.0.0', port=8000)
