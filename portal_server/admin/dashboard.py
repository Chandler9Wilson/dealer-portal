from flask import Blueprint, redirect, url_for

# flask-login used for login management and persistence
from flask_login import current_user

# flask-principal is used for per resource control and permissions
from flask_principal import Principal, Permission, RoleNeed

admin_role = Permission(RoleNeed('admin'))

admin = Blueprint('admin', __name__)


@admin.route('/', methods=['GET'])
@admin_role.require(http_exception=403)
def serve_admin_dashboard():
    return 'This is the dashboard'


@admin.errorhandler(403)
def forbidden(error):
    # TODO create error pages and change both of these to use that

    if current_user:
        # This response should be a 403 error page
        return redirect(url_for('directory.home'))
    else:
        # This response should be a 401 error page
        return redirect(url_for('login_bp.login'))
