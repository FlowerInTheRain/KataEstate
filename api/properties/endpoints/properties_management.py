from datetime import date

from flask import jsonify, request, current_app, Response
from flask_restx import Resource, Namespace, api, fields

from properties.repositories import QueryProperties
from properties.models.Properties import Properties
from properties.repositories import CommandProperties

from properties.models.PropertyStatuses import PropertyStatuses
from properties.models.PropertyTypes import PropertyTypes
from werkzeug.exceptions import BadRequest

from properties.models.Properties import Property

from properties.mappers.with_id_to_db import from_json

ns = Namespace('properties', description='base healthcheck test operations')

property_model = ns.model('Property', {
    'id': fields.Integer,
    'address': fields.String,
    'type': fields.String,
    'status': fields.String,
    'purchase_date': fields.String,
    'price': fields.Integer
})

add_property_model = ns.model('AddProperty', {
    'address': fields.String(required=True, min_length=10),
    'type': fields.String(required=True, enum=[e.value for e in PropertyTypes]),
    'status': fields.String(required=True, enum=[e.value for e in PropertyStatuses]),
    'purchase_date': fields.String,
    'price': fields.Integer(required=True, min=0)
})

@ns.route("/")
class BasePath(Resource):
    @ns.marshal_with(property_model, as_list=True)
    def get(self):  # put application's code here
        return QueryProperties.get_all_properties()
    @ns.expect(add_property_model, validate=True)
    def post(self):
        new_property = Properties(request.json["address"],
                                  PropertyTypes(request.json["type"]),
                                  PropertyStatuses(request.json["status"]),
                                  request.json["purchase_date"],
                                  request.json["price"])
        purchase_date = date.fromisoformat(request.json["purchase_date"])
        if purchase_date < date.today():
            return CommandProperties.create_property(new_property)
        else:
            return Response(status=400)
    @ns.expect(property_model, validate=True)
    def put(self):
        current_property = from_json(request.json)
        purchase_date = current_property.purchase_date
        if purchase_date < date.today():
            CommandProperties.update_property(current_property)
            return Response(status=204)
        else:
            return Response(status=400)

@ns.route('/<int:property_id>')
class ByID(Resource):
    def delete(self, property_id: int):
        CommandProperties.delete_property(property_id)
        return Response(status=204)
