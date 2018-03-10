from flask import Blueprint

api = Blueprint('api', __name__)


def get_items(db_class):
    """Retrieves up to the first 500 items of a db_class defined in models"""
    item_list = db_class.query.limit(500).all()
    # Really a list of dictionaries but couldn't think of a better name
    item_dicts = []

    for item in item_list:
        item_dicts.append(db_class.as_dict(item))

    # TODO Might want to move jsonify to the view function?
    return jsonify(item_dicts)


@api.route('/customers/', methods=['GET'])
@api.route('/customers/<int:customer_id>/', methods=['GET'])
def get_customers(customer_id=None):

    # GET a list of up to the first 20 customers
    customer_json = get_items(Customer)

    return customer_json


@api.route('/customers/<int:customer_id>/facilities/', methods=['GET'])
@api.route('/customers/<int:customer_id>/facilities/<int:facility_id>/',
           methods=['GET'])
def get_nested():
    return None


# TODO custom messages https://stackoverflow.com/a/21301229/6879253


@api.errorhandler(400)
def not_found(error):
    # Handle 400 errors so that they make more sense for the api
    # TODO make this error a bit more descriptive

    return make_response(jsonify({'error': 'Failed to decode'}), 400)


@api.errorhandler(404)
def not_found(error):
    # Handle 404 errors so that they make more sense for the api
    # TODO make this error a bit more descriptive

    return make_response(jsonify({'error': 'Not found'}), 404)


@api.errorhandler(415)
def not_found(error):
    # Handle 415 errors so that they make more sense for the api
    # TODO make this error a bit more descriptive

    return make_response(
        jsonify({'error': 'You sent an unsupported media type'}), 415)


@api.errorhandler(500)
def not_found(error):
    # Handle 500 errors so that they make more sense for the api
    # This will not work properly when debug=true
    # TODO make this error a bit more descriptive

    return make_response(jsonify({'error': 'Internal server error'}), 500)
