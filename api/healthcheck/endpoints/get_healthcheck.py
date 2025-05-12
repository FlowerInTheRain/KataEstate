from flask import jsonify
from flask_restx import Resource, Namespace

ns = Namespace('healthcheck', description='base healthcheck test operations')

@ns.route('/')
class HealthCheck(Resource):
    def get(self):  # put application's code here
        return "Hello World!"

@ns.route('/json')
class Json(Resource):
    def get(self):  # put application's code here
        return jsonify({"num":5})

