from datetime import date, datetime
from typing import List

from flask import request, current_app, Blueprint
from flask_pydantic_spec import Request, Response
from flask_restx import Resource, Namespace, fields
from flask_restx.fields import Integer
from maintenances.models.MaintenanceStatuses import MaintenanceStatuses
from maintenances.models.Maintenances import Maintenances, Maintenance
from maintenances.repositories import CommandMaintenances, QueryMaintenances
from pydantic import BaseModel, RootModel, constr

from app import spec
from constants import API_base_path, PositiveInt, CreateItemResponse

maintenances_blueprint = Blueprint('maintenances management', __name__,
                                 url_prefix=API_base_path + '/properties')

class MaintenanceDTO(BaseModel):
    id: PositiveInt
    task_description: str
    status: str
    scheduled_date: str
    property_id: PositiveInt

class CreateMaintenanceRequest(BaseModel):
    id: PositiveInt
    task_description: constr(min_length=5, max_length=50)
    status: MaintenanceStatuses
    scheduled_date: constr(min_length=10, max_length=10)
    property_id: PositiveInt

class UpdateMaintenanceRequest(BaseModel):
    id: PositiveInt
    task_description: str
    status: str
    scheduled_date: str
    property_id: PositiveInt

class MaintenancesResponse(RootModel):
    root: List[MaintenanceDTO]



@maintenances_blueprint.route("/", methods=["GET"])
@spec.validate(body=Request(), resp=Response(HTTP_200=MaintenancesResponse))
def get():  # put application's code here
    data = QueryMaintenances.get_all_maintenance_tasks()
    for task in data:
        current_app.logger.info(task)
    return data

@maintenances_blueprint.route("/", methods=["POST"])
@spec.validate(body=Request(CreateMaintenanceRequest), resp=Response(HTTP_201=CreateItemResponse))
def post():
    new_task = Maintenances(
        request.json["task_description"],
        MaintenanceStatuses(request.json["status"]),
        request.json["scheduled_date"],
        request.json["property_id"])
    return CommandMaintenances.create_maintenance_task(new_task), 201


@maintenances_blueprint.route("/", methods=["PUT"])
@spec.validate(body=Request(UpdateMaintenanceRequest), resp=Response())
def put():
    current_tenant = from_json(request.json)
    CommandMaintenances.update_maintenance_task(current_tenant)
    return Response(status=204)


@maintenances_blueprint.route("/<int:task_id>", methods=["DELETE"])
def delete(task_id: Integer):
    CommandMaintenances.delete_maintenance_task(task_id)
    return Response(status=204)

def from_json(json):
    mapped_task = Maintenance()
    mapped_task.id = json["id"]
    mapped_task.task_description = json["task_description"]
    mapped_task.status = MaintenanceStatuses(json["status"]).value
    mapped_task.scheduled_date = datetime.strptime(json["scheduled_date"], "%Y-%m-%d").date()
    mapped_task.property_id = json["property_id"]
    return mapped_task
