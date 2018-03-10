# This script needs to be run in the venv from ./ as python -m db.setup
# Documentation on why above is needed \
# https://stackoverflow.com/a/28154841/6879253

from db.models import db
from run import app

with app.test_request_context():
    db.init_app(app)

    db.create_all()
