# TODO sort imports https://stackoverflow.com/a/20763446/6879253
from flask import Flask, render_template, make_response
from flask import session as login_session
import random
import string
import json
import httplib2
import requests

# TODO update to a different library oauth2client is depreciated
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

app = Flask(__name__)


@app.route('/')
def login():
    # TODO change route to /login

    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # render the login template with the template variable state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response('Hello World!', 200)
        return response


if __name__ == '__main__':
    # TODO change secret_key
    app.secret_key = 'super secret key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
