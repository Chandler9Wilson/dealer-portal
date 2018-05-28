from flask import Blueprint, send_from_directory

# flask-login used for login management and persistence
from flask_login import login_required

directory = Blueprint('directory', __name__,
                      static_folder='home_static/dist',
                      template_folder='templates')


@directory.route('/', methods=['GET'])
@directory.route('/<path:filename>', methods=['GET'])
@login_required
def home(filename='index.html'):
    return send_from_directory(directory.static_folder, filename)
