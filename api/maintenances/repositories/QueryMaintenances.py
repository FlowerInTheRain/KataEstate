from db import session

from maintenances.models.Maintenances import Maintenance


def get_all_maintenance_tasks():
    return session.query(Maintenance).order_by(Maintenance.id).all()