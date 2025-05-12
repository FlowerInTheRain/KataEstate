from typing import List

from db import session
from sqlalchemy import text

from maintenances.models.Maintenances import Maintenance


def bulk_create_maintenances(maintenances: List[Maintenance]):
    session.bulk_save_objects(maintenances)
    session.commit()

def cleanup_maintenances():
    session.execute(text('DELETE FROM maintenances;'))

