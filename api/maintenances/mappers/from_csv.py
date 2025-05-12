from datetime import datetime

from maintenances.models.MaintenanceStatuses import MaintenanceStatuses
from maintenances.models.Maintenances import Maintenance


def to_db_maintenance(row):
    new_maintenance = Maintenance()
    new_maintenance.id = row["TaskID"]
    new_maintenance.task_description = row["Description"]
    new_maintenance.status = MaintenanceStatuses(row["Status"]).value
    new_maintenance.scheduled_date = datetime.strptime(row["ScheduledDate"], "%Y-%m-%d").date()
    new_maintenance.property_id = int(row["PropertyID"])
    return new_maintenance