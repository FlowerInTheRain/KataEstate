from typing import List

from db import session
from flask import current_app
from sqlalchemy import Integer
from tenants.models.Tenants import Tenant
from tenants.models.Tenants import Tenants


def bulk_create_tenants( tenants: List[Tenant]):
    session.bulk_save_objects(tenants)
    session.commit()


def create_tenant(new_tenant: Tenants):
    to_db = Tenant()
    to_db.name = new_tenant.name
    to_db.contact_info = new_tenant.contact_info
    to_db.lease_term_start = new_tenant.lease_term_start
    to_db.lease_term_end = new_tenant.lease_term_end
    to_db.rent_paid = new_tenant.rent_paid.value
    to_db.id = None
    to_db.property_id = new_tenant.property_id
    session.add(to_db)
    session.commit()
    return to_db.id


def update_tenant(updated_tenant: Tenant):
    current_app.logger.info(updated_tenant)
    in_db = session.get(Tenant, updated_tenant.id)
    in_db.name = updated_tenant.name
    in_db.contact_info = updated_tenant.contact_info
    in_db.lease_term_start = updated_tenant.lease_term_start
    in_db.lease_term_end = updated_tenant.lease_term_end
    in_db.rent_paid = updated_tenant.rent_paid
    session.commit()


def delete_tenant(to_delete: Integer):
    in_db = session.get(Tenant, to_delete)
    session.delete(in_db)
    session.commit()
