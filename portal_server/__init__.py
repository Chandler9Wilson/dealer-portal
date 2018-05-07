import os

from flask import Flask, url_for, redirect

# flask-login used for login management and persistence
from flask_login import LoginManager, current_user

# flask-principal is used for per resource control and permissions
from flask_principal import Principal, identity_loaded, RoleNeed, UserNeed

# Import database classes and SQLAlchamy instance
from portal_server.db.models import db, User

# Blueprint imports
from portal_server.api.endpoints import api
from portal_server.login_management.login import login_bp
from portal_server.directory.home import directory
from portal_server.admin.dashboard import admin
from portal_server.admin.management import admin_api

config = {
    'development': 'portal_server.config.DevelopmentConfig',
    'testing': 'portal_server.config.TestingConfig',
    'production': 'portal_server.config.ProductionConfig',
    'default': 'portal_server.config.DevelopmentConfig'
}


def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(config[config_name])


# Flask config
app = Flask(__name__)
configure_app(app)

# Flask-Login class
login_manager = LoginManager()
login_manager.login_view = 'login_bp.login'
login_manager.init_app(app)

# Flask-principal load
principals = Principal(app)


@login_manager.user_loader
def load_user(id):
    """This is a user loader used by flask-login"""
    return User.query.filter_by(id=id).first()


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.title))


# Register blueprints
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(directory, url_prefix='/home')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(admin_api, url_prefix='/admin/api')
app.register_blueprint(login_bp)

# Starts up flask-sqlalchemy
db.init_app(app)


@app.errorhandler(404)
def not_found(error):
    # Handle 404 errors so that they make more sense for the api
    # TODO make this error a bit more descriptive

    return redirect(url_for('login_bp.login'))
