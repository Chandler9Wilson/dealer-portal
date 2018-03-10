import os

from flask import Flask

# TODO eval if this needs to be here
# Import database classes and SQLAlchamy instance
from portal_server.db.models import db

from portal_server.api.endpoints import api

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')

# TODO make config options more succinct
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://catalog:catalog@' + \
    'localhost:5432/acmonitor'
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

# TODO this needs a better name
# Begin flask modifications


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
