from typing import List

from db import session
from flask import current_app
from sqlalchemy import text, Integer

from maintenances.models.Maintenances import Maintenance
from maintenances.models.Maintenances import Maintenances



def bulk_create_maintenances(maintenances: List[Maintenance]):
    session.bulk_save_objects(maintenances)
    session.commit()

def create_maintenance_task(new_maintenance_task: Maintenances):
    current_app.logger.info(new_maintenance_task)
    to_db = Maintenance()
    to_db.task_description = new_maintenance_task.task_description
    to_db.status = new_maintenance_task.status.value
    to_db.scheduled_date = new_maintenance_task.scheduled_date
    to_db.property_id = new_maintenance_task.property_id
    to_db.id = None
    current_app.logger.info(to_db)
    session.add(to_db)
    session.commit()
    return to_db.id

def update_maintenance_task(updated_maintenance_task: Maintenance):
    current_app.logger.info(updated_maintenance_task)
    in_db = session.get(Maintenance, updated_maintenance_task.id)
    in_db.task_description = updated_maintenance_task.task_description
    in_db.status = updated_maintenance_task.status
    in_db.scheduled_date = updated_maintenance_task.scheduled_date
    session.commit()


def delete_maintenance_task(to_delete: Integer):
    in_db = session.get(Maintenance, to_delete)
    session.delete(in_db)
    session.commit()

