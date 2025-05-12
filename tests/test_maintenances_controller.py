import pytest
from datetime import date, timedelta
from unittest.mock import patch, MagicMock

from maintenances.models.MaintenanceStatuses import MaintenanceStatuses

from maintenances.models.Maintenances import Maintenance


@pytest.fixture
def valid_create_maintenance_task_payload():
    return {
        "task_description": "Sid Bennaceur",
        "status": MaintenanceStatuses.PENDING.value,
        "scheduled_date": str(date.today() + timedelta(days=10)),
        "property_id": 1
    }

@pytest.fixture
def valid_maintenance_task_update_payload(valid_maintenance_task_payload):
    update_tenant_payload = valid_maintenance_task_payload.copy()
    update_tenant_payload["id"] = 1
    return update_tenant_payload


# ---------- GET ----------
@patch("maintenances.repositories.QueryMaintenances.get_all_maintenance_tasks")
def test_get_tasks_returns_list(mock_get, client):
    mock_get.return_value = [
        Maintenance(
            id=1,
            task_description="Sid Bennaceur",
            status=MaintenanceStatuses.PENDING.value,
            scheduled_date="2025-06-30",
            property_id=1
        )
    ]
    res = client.get("/app/maintenances/")
    assert res.status_code == 200
    data = res.get_json()
    print(data[0]["task_description"])
    print("lol")
    assert isinstance(data, list)
    assert data[0]["task_description"] == "Sid Bennaceur"


# ---------- POST ----------
@patch("maintenances.repositories.CommandMaintenances.create_maintenance_task")
def test_post_task_valid(mock_create, client, valid_task_payload):
    mock_create.return_value = 1
    res = client.post("/app/maintenances/", json=valid_task_payload)
    assert res.status_code == 200
    assert res.get_json() == mock_create.return_value
    mock_create.assert_called_once()


def test_post_task_invalid_date(client, valid_tenant_payload):
    # Lease end before start
    valid_tenant_payload["scheduled_date"] = str(date.today() - timedelta(days=20))
    res = client.post("/app/maintenances/", json=valid_tenant_payload)
    assert res.status_code == 400


# ---------- PUT ----------
@patch("maintenances.repositories.CommandMaintenances.update_maintenance_task")

def test_put_task_valid(mock_update, client, valid_tenant_update_payload):
    res = client.put("/app/maintenances/", json=valid_tenant_update_payload)
    assert res.status_code == 204
    mock_update.assert_called_once()


def test_put_task_invalid_date(client, valid_tenant_update_payload):
    valid_tenant_update_payload["scheduled_date"] = str(date.today() - timedelta(days=20))
    res = client.put("/app/maintenances/", json=valid_tenant_update_payload)
    assert res.status_code == 400


# ---------- DELETE ----------
@patch("maintenances.repositories.CommandMaintenances.delete_maintenance_task")
def test_delete_maintenance(mock_delete, client):
    res = client.delete("/app/maintenances/1")
    assert res.status_code == 204
    mock_delete.assert_called_once_with(1)
