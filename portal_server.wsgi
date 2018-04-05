activate_this = '/home/chandler/dealer-portal/env/bin/activate'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from portal_server import app as application