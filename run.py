import random
import string
import json

from flask import Flask, session, render_template, request

# used for google oauth verification of tokens
from google.oauth2 import id_token
from google.auth.transport import requests as googleRequests

# makes sure this is different from the main files flask name or cookies
# etc will be shared
app2 = Flask(__name__)


@app2.route('/setuser/<user>')
def setuser(user):
    print '-' * 30
    print request.headers
    print '-' * 30
    print session

    infoMessage = 'User value set to: ' + \
        session['user']
    return render_template('login.html', debugIt=infoMessage)


@app2.route('/getuser')
def getuser():
    print session

    infoMessage = 'User value set to: ' + \
        session['user']
    return infoMessage


@app2.route('/gconnect', methods=['POST'])
def gconnect():

    CLIENT_ID = '349469004723-j9csi1hlhb1s0abuap24lo50mgvbkrhh.apps.googleusercontent.com'
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
        pass

    return 'hello world'


if __name__ == '__main__':
    # TODO change secret_key
    app2.secret_key = 'super secret key'
    app2.debug = True
    app2.run(host='0.0.0.0', port=8000)
