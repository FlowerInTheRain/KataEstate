from datetime import datetime

from properties.models.PaymentStatuses import PaymentStatuses
from tenants.models.Tenants import Tenant


def to_db_tenant(row):
    new_tenant = Tenant()
    new_tenant.id = row["TenantID"]
    new_tenant.name = row["Name"]
    new_tenant.contact_info = row["ContactInfo"]
    new_tenant.lease_term_start = datetime.strptime(row["LeaseTermStart"], "%Y-%m-%d").date()
    new_tenant.lease_term_end = datetime.strptime(row["LeaseTermEnd"], "%Y-%m-%d").date()
    new_tenant.rent_paid = PaymentStatuses(row["RentalPaymentStatus"]).value
    new_tenant.property_id = int(row["PropertyID"])
    return new_tenant