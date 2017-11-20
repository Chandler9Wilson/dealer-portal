from flask import Flask
from flask import session as login_session
import random
import string

app = Flask(__name__)


@app.route("/")
def login():
    # TODO change route to /login
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return "The current session state is %s" % login_session['state']


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
