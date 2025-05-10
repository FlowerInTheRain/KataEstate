from datetime import datetime

from maintenances.models.MaintenanceStatuses import MaintenanceStatuses
from maintenances.models.Maintenances import Maintenance


def to_db_maintenance(row):
    new_maintenance = Maintenance()
    new_maintenance.task_description = row[1]
    new_maintenance.status = MaintenanceStatuses(row[2]).value
    new_maintenance.scheduled_date = datetime.strptime(row[3], "%Y-%m-%d").date()
    new_maintenance.property_id = int(row[4])
    return new_maintenance