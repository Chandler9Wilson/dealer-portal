import os

from flask import Flask, url_for, redirect

# flask-login used for login management and persistence
from flask_login import LoginManager

# Import database classes and SQLAlchamy instance
from portal_server.db.models import db, User

# Blueprint imports
from portal_server.api.endpoints import api
from portal_server.login_management.login import login_bp
from portal_server.directory.home import directory

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


@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


# Register blueprints
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(directory, url_prefix='/home')
app.register_blueprint(login_bp)

# Starts up flask-sqlalchemy
db.init_app(app)


@app.errorhandler(404)
def not_found(error):
    # Handle 404 errors so that they make more sense for the api
    # TODO make this error a bit more descriptive

    return redirect(url_for('login_bp.login'))
