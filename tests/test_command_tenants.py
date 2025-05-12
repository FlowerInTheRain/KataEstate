from unittest.mock import patch, MagicMock

import pytest
from tenants.models.Tenants import Tenant, Tenants
from tenants.repositories.CommandTenants import (
    bulk_create_tenants,
    create_tenant,
    update_tenant,
    delete_tenant
)

from api.properties.models.PaymentStatuses import PaymentStatuses


@pytest.mark.usefixtures("app_context")

@patch("tenants.repositories.CommandTenants.session")
def test_bulk_create_tenants(mock_session):
    tenants = [MagicMock(spec=Tenant), MagicMock(spec=Tenant)]
    bulk_create_tenants(tenants)
    mock_session.bulk_save_objects.assert_called_once_with(tenants)
    mock_session.commit.assert_called_once()

@pytest.mark.usefixtures("app_context")
@patch("tenants.repositories.CommandTenants.session")
def test_create_tenant_returns_id(mock_session):
    mock_added_tenant = MagicMock()
    mock_added_tenant.id = 42
    mock_session.add.side_effect = lambda obj: setattr(obj, "id", 42)

    new = Tenants(
        name="Sid Bennaceur",
        contact_info="+33764017528",
        lease_term_start="2023-01-01",
        lease_term_end="2024-01-01",
        rent_paid=PaymentStatuses.PAID,
        property_id=3
    )

    result_id = create_tenant(new)

    assert result_id == 42
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


@patch("tenants.repositories.CommandTenants.session")
@patch("tenants.repositories.CommandTenants.current_app")
def test_update_tenant(mock_1, mock_session):
    existing = MagicMock(spec=Tenant)
    mock_session.get.return_value = existing

    updated = MagicMock(spec=Tenant)
    updated.id = 1
    updated.name = "Sid Bennaceur"
    updated.contact_info = "sa.bennaceur@example.com"
    updated.lease_term_start = "2022-05-01"
    updated.lease_term_end = "2023-05-01"

    update_tenant(updated)

    assert existing.name == updated.name
    assert existing.contact_info == updated.contact_info
    assert existing.lease_term_start == updated.lease_term_start
    assert existing.lease_term_end == updated.lease_term_end
    mock_session.commit.assert_called_once()

@patch("tenants.repositories.CommandTenants.session")
def test_delete_tenant(mock_session):
    mock_existing = MagicMock(spec=Tenant)
    mock_session.get.return_value = mock_existing

    delete_tenant(42)

    mock_session.get.assert_called_once_with(Tenant, 42)
    mock_session.delete.assert_called_once_with(mock_existing)
    mock_session.commit.assert_called_once()
