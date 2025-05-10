from typing import List
from sqlalchemy import text
from db import session
from tenants.models.Tenants import Tenant


def cleanup_tenants():
    session.execute(text('DELETE FROM tenants;'))

def bulk_create_tenants( tenants: List[Tenant]):
    session.bulk_save_objects(tenants)
    session.commit()
