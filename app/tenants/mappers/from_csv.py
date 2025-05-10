from datetime import datetime

from properties.models.PaymentStatuses import PaymentStatuses
from tenants.models.Tenants import Tenant


def to_db_tenant(row):
    new_tenant = Tenant()
    new_tenant.name = row[1]
    new_tenant.contact_info = row[2]
    new_tenant.lease_term_start = datetime.strptime(row[3], "%Y-%m-%d").date()
    new_tenant.lease_term_end = datetime.strptime(row[4], "%Y-%m-%d").date()
    new_tenant.rent_paid = PaymentStatuses(row[5]).value
    new_tenant.property_id = int(row[6])
    return new_tenant