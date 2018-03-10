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


@app.route('/customers/', methods=['GET'])
@app.route('/customers/<int:customer_id>/', methods=['GET'])
def get_customers(customer_id=None):

    # GET a list of up to the first 20 customers
    customer_json = get_items(Customer)

    return customer_json


@app.route('/customers/<int:customer_id>/facilities/', methods=['GET'])
@app.route('/customers/<int:customer_id>/facilities/<int:facility_id>/',
           methods=['GET'])
def get_nested():
    return None
