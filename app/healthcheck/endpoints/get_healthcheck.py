from flask import jsonify
from flask.sansio.blueprints import Blueprint

from constants import API_base_path

ns = Blueprint('healthcheck',__name__,
                                 url_prefix=API_base_path + '/properties')

@ns.route('/', methods=['GET'])
def get(self):  # put application's code here
    return "Hello World!"

@ns.route('/json', methods=['GET'])
def get():  # put application's code here
    return jsonify({"num":5})

