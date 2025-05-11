from db import session

from tenants.models.Tenants import Tenant


def get_all_tenants():
    return session.query(Tenant).order_by(Tenant.id).all()