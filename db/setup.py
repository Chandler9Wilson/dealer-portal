# this assumes that setup_script.sh has been run
# also for SELECT privileges https://serverfault.com/a/284278t

from db.models import db
from run import app

with app.test_request_context():
     db.init_app(app)

     db.create_all()
