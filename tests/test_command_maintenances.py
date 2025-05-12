from datetime import date
from unittest.mock import MagicMock, patch

import pytest

from maintenances.models.MaintenanceStatuses import MaintenanceStatuses
from maintenances.models.Maintenances import Maintenance, Maintenances
from maintenances.repositories.CommandMaintenances import bulk_create_maintenances, create_maintenance_task, \
    update_maintenance_task, delete_maintenance_task


@pytest.mark.usefixtures("app_context")

@patch("maintenances.repositories.CommandMaintenances.session")
def test_bulk_create_tenants(mock_session):
    maintenances = [MagicMock(spec=Maintenance), MagicMock(spec=Maintenance)]
    bulk_create_maintenances(maintenances)
    mock_session.bulk_save_objects.assert_called_once_with(maintenances)
    mock_session.commit.assert_called_once()

@pytest.mark.usefixtures("app_context")
@patch("maintenances.repositories.CommandMaintenances.session")
def test_create_tenant_returns_id(mock_session):
    mock_added_tenant = MagicMock()
    mock_added_tenant.id = 42
    mock_session.add.side_effect = lambda obj: setattr(obj, "id", 42)

    new = Maintenances(
        task_description="Sid Bennaceur",
        status=MaintenanceStatuses.PENDING,
        scheduled_date= date.fromisoformat("2023-01-01"),
        property_id=3
    )

    result_id = create_maintenance_task(new)

    assert result_id == 42
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


@patch("maintenances.repositories.CommandMaintenances.session")
@patch("maintenances.repositories.CommandMaintenances.current_app")
def test_update_task(mock_1, mock_session):
    existing = MagicMock(spec=Maintenance)
    existing.id = 1
    mock_session.get.return_value = existing

    updated = MagicMock(spec=Maintenance)
    updated.id = 1
    updated.task_description = "Sid Bennaceur"

    update_maintenance_task(updated)

    assert existing.task_description == updated.task_description
    assert existing.id == updated.id
    mock_session.commit.assert_called_once()

@patch("maintenances.repositories.CommandMaintenances.session")
def test_delete_tenant(mock_session):
    mock_existing = MagicMock(spec=Maintenance)
    mock_session.get.return_value = mock_existing

    delete_maintenance_task(42)

    mock_session.get.assert_called_once_with(Maintenance, 42)
    mock_session.delete.assert_called_once_with(mock_existing)
    mock_session.commit.assert_called_once()
