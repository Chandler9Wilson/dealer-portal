from flask import Blueprint, make_response, jsonify

# flask-principal is used for per resource control and permissions
from flask_principal import Principal, Permission, RoleNeed

admin_role = Permission(RoleNeed('admin'))

admin_api = Blueprint('admin_api', __name__)


@admin_api.route('/', methods=['GET'])
@admin_role.require(http_exception=403)
def serve_admin_list():
    return 'This is the admin api'


@admin_api.errorhandler(403)
def forbidden(error):
    # TODO make this error a bit more descriptive
    generic_message = 'Forbidden, you do not have the ' + \
        'role needed to access this resource'

    return make_response(jsonify({'error': generic_message}), 403)
