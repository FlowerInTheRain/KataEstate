from unittest.mock import patch, MagicMock

from tenants.models.Tenants import Tenant, Tenants
from tenants.repositories.CommandTenants import (
    bulk_create_tenants,
    create_tenant,
    update_tenant,
    delete_tenant
)


@patch("tenants.repositories.CommandTenants.session")
def test_bulk_create_tenants(mock_session):
    tenants = [MagicMock(spec=Tenant), MagicMock(spec=Tenant)]
    bulk_create_tenants(tenants)
    mock_session.bulk_save_objects.assert_called_once_with(tenants)
    mock_session.commit.assert_called_once()

@patch("tenants.repositories.CommandTenants.session")
def test_create_tenant(mock_session):
    new = MagicMock(spec=Tenants)
    new.name = "Sid Bennaceur"
    new.contact_info = "+33764017528"
    new.lease_term_start = "2023-01-01"
    new.lease_term_end = "2024-01-01"
    new.rent_paid.value = "Paid"

    mock_session.add = MagicMock()
    mock_session.commit = MagicMock()

    with patch("tenants.repositories.CommandTenants.Tenant") as mock_tenant_class:
        mock_instance = mock_tenant_class.return_value
        mock_instance.id = 123  # simulate returned ID

        tenant_id = create_tenant(new)

        assert tenant_id == 123
        assert mock_instance.name == new.name
        assert mock_instance.contact_info == new.contact_info
        assert mock_instance.lease_term_start == new.lease_term_start
        assert mock_instance.lease_term_end == new.lease_term_end
        assert mock_instance.rent_paid == new.rent_paid.value

        mock_session.add.assert_called_once_with(mock_instance)
        mock_session.commit.assert_called_once()

@patch("tenants.repositories.CommandTenants.session")
@patch("tenants.repositories.CommandTenants.current_app")
def test_update_tenant(mock_app, mock_session):
    existing = MagicMock(spec=Tenant)
    mock_session.get.return_value = existing

    updated = MagicMock(spec=Tenant)
    updated.id = 1
    updated.name = "Sid Bennaceur"
    updated.contact_info = "sa.bennaceur@example.com"
    updated.lease_term_start = "2022-05-01"
    updated.lease_term_end = "2023-05-01"
    updated.rent_paid.value = "Pending"

    update_tenant(updated)

    assert existing.name == updated.name
    assert existing.contact_info == updated.contact_info
    assert existing.lease_term_start == updated.lease_term_start
    assert existing.lease_term_end == updated.lease_term_end
    assert existing.rent_paid == updated.rent_paid.value
    mock_session.commit.assert_called_once()

@patch("tenants.repositories.CommandTenants.session")
def test_delete_tenant(mock_session):
    mock_existing = MagicMock(spec=Tenant)
    mock_session.get.return_value = mock_existing

    delete_tenant(42)

    mock_session.get.assert_called_once_with(Tenant, 42)
    mock_session.delete.assert_called_once_with(mock_existing)
    mock_session.commit.assert_called_once()
