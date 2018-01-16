# this assumes that setup_script.sh has been run
# also for SELECT privileges https://serverfault.com/a/284278
# TODO improve security for deployment

import sys
sys.path.insert(0, "/home/to/your/package_or_module")

from catalog import run
db.create_all()
