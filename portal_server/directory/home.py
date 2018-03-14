from flask import Blueprint, render_template

# flask-login used for login management and persistence
from flask_login import login_required

directory = Blueprint('directory', __name__,
                      static_folder='home_static',
                      template_folder='templates')


@directory.route('/')
@login_required
def home():
    return render_template('directory.html')
