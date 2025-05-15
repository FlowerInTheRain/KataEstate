from datetime import date

from constants import API_base_path
from flask import Blueprint, request
from flask_pydantic_spec import Request, Response
from properties.mappers.with_id_to_db import from_json
from properties.models.Properties import Properties
from properties.models.Properties import Property
from properties.models.PropertyStatuses import PropertyStatuses
from properties.models.PropertyTypes import PropertyTypes
from properties.models.dtos.property_dtos import (PropertyResponse, AddPropertyRequest,
                                                  PropertyRequest)
from properties.repositories import CommandProperties
from properties.repositories import QueryProperties

from app import spec
from constants import CreateItemResponse

properties_blueprint = Blueprint('properties management', __name__,
                                 url_prefix=API_base_path + '/properties')




@properties_blueprint.route("/", methods=["GET"])
@spec.validate(body=Request(), resp=Response(HTTP_200=PropertyResponse))
def get_all_properties():  # put application's code here
    return [p.dict() for p in QueryProperties.get_all_properties()], 200

@properties_blueprint.route("/", methods=["POST"])
@spec.validate(body=Request(AddPropertyRequest), resp=Response(HTTP_201=CreateItemResponse))
def create_property():
    data = request.get_json()
    new_property = Property(**data)
    purchase_date = date.fromisoformat(request.json["purchase_date"])
    if purchase_date < date.today():
        return CommandProperties.create_property(new_property), 201
    else:
        return Response(status=400)

@properties_blueprint.route("/", methods=["PUT"])
@spec.validate(body=Request(PropertyRequest), resp=Response())
def update_property():
    current_property = from_json(request.json)
    purchase_date = current_property.purchase_date
    if purchase_date < date.today():
        CommandProperties.update_property(current_property)
        return Response(status=204)
    else:
        return Response(status=400)

@properties_blueprint.route('/<int:property_id>', methods=["DELETE"])
def delete_property(property_id: int):
    CommandProperties.delete_property(property_id)
    return Response(status=204)
