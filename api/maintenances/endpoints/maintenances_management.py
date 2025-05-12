from datetime import date, datetime

from flask import request, current_app, Response
from flask_restx import Resource, Namespace, fields
from flask_restx.fields import Integer
from maintenances.models.MaintenanceStatuses import MaintenanceStatuses
from maintenances.models.Maintenances import Maintenances, Maintenance
from maintenances.repositories import CommandMaintenances, QueryMaintenances

ns = Namespace('maintenances', description='CRUD Operations on maintenance tasks')

maintenance_task_model = ns.model('Maintenance', {
    'id': fields.Integer,
    'task_description': fields.String,
    'status': fields.String(required=True, enum=[e.value for e in MaintenanceStatuses]),
    'scheduled_date': fields.String,
    'property_id': fields.Integer
})

add_maintenance_task_model = ns.model('AddMaintenanceTask', {
    'task_description': fields.String,
    'status': fields.String(required=True, enum=[e.value for e in MaintenanceStatuses]),
    'scheduled_date': fields.String,
    'property_id': fields.Integer
})


@ns.route("/")
class BasePath(Resource):
    @ns.marshal_with(maintenance_task_model, as_list=True)
    def get(self):  # put application's code here
        data = QueryMaintenances.get_all_maintenance_tasks()
        for task in data:
            current_app.logger.info(task)
        return data

    @ns.expect(add_maintenance_task_model, validate=True)
    def post(self):
        new_task = Maintenances(
            request.json["task_description"],
            MaintenanceStatuses(request.json["status"]),
            request.json["scheduled_date"],
            request.json["property_id"])
        return CommandMaintenances.create_maintenance_task(new_task)


    @ns.expect(maintenance_task_model, validate=True)
    def put(self):
        current_tenant = from_json(request.json)
        CommandMaintenances.update_maintenance_task(current_tenant)
        return Response(status=204)


@ns.route('/<int:task_id>')
class ByID(Resource):
    def delete(self, task_id: Integer):
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
