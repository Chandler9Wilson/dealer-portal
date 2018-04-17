import os

from flask import Flask, url_for, redirect

# flask-login used for login management and persistence
from flask_login import LoginManager

# Import database classes and SQLAlchamy instance
from portal_server.db.models import db, User

from secrets import db_username, db_password

# Blueprint imports
from portal_server.api.endpoints import api
from portal_server.login_management.login import login_bp
from portal_server.directory.home import directory

# Flask config
app = Flask(__name__)
# TODO make config options more succinct
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + db_username + ':' + \
    db_password + '@localhost:5432/acmonitor'
app.secret_key = 'super secret key'

# Flask-Login class
login_manager = LoginManager()
login_manager.login_view = 'login_bp.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


# Register blueprints
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(directory, url_prefix='/home')
app.register_blueprint(login_bp)

# Starts up flask-sqlalchemy
db.init_app(app)


@app.context_processor
# TODO remove before deployment
def override_url_for():
    """Generate a new token on every request to prevent the browser from
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


@app.errorhandler(404)
def not_found(error):
    # Handle 404 errors so that they make more sense for the api
    # TODO make this error a bit more descriptive

    return redirect(url_for('login_bp.login'))
