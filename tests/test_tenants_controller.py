import pytest
from datetime import date, timedelta
from unittest.mock import patch, MagicMock

from properties.models.PaymentStatuses import PaymentStatuses

from tenants.models.Tenants import Tenant


@pytest.fixture
def valid_tenant_payload():
    return {
        "name": "Sid Bennaceur",
        "contact_info": "+33764017528",
        "lease_term_start": str(date.today() - timedelta(days=10)),
        "lease_term_end": str(date.today() + timedelta(days=10)),
        "rent_paid": PaymentStatuses.PAID.value,
        "property_id": 1
    }

@pytest.fixture
def valid_tenant_update_payload(valid_tenant_payload):
    payload = valid_tenant_payload.copy()
    payload["id"] = 1
    return payload


# ---------- GET ----------
@patch("tenants.repositories.QueryTenants.get_all_tenants")
def test_get_tenants_returns_list(mock_get, client):
    mock_get.return_value = [
        Tenant(
            id=1,
            name="Sid Bennaceur",
            contact_info="+33764017528",
            lease_term_start="2025-04-16",
            lease_term_end="2035-04-16",
            rent_paid="Paid",
            property_id=1
        )
    ]
    res = client.get("/api/tenants/")
    assert res.status_code == 200
    data = res.get_json()
    print(data[0]["name"])
    print("lol")
    assert isinstance(data, list)
    assert data[0]["name"] == "Sid Bennaceur"


# ---------- POST ----------
@patch("tenants.repositories.CommandTenants.create_tenant")
def test_post_tenant_valid(mock_create, client, valid_tenant_payload):
    mock_create.return_value = 1
    res = client.post("/api/tenants/", json=valid_tenant_payload)
    assert res.status_code == 200
    assert res.get_json() == mock_create.return_value
    mock_create.assert_called_once()


def test_post_tenant_invalid_date(client, valid_tenant_payload):
    # Lease end before start
    valid_tenant_payload["lease_term_end"] = str(date.today() - timedelta(days=20))
    res = client.post("/api/tenants/", json=valid_tenant_payload)
    assert res.status_code == 400


# ---------- PUT ----------
@patch("tenants.repositories.CommandTenants.update_tenant")
def test_put_tenant_valid(mock_update, client, valid_tenant_update_payload):
    res = client.put("/api/tenants/", json=valid_tenant_update_payload)
    assert res.status_code == 204
    mock_update.assert_called_once()


def test_put_tenant_invalid_date(client, valid_tenant_update_payload):
    valid_tenant_update_payload["lease_term_end"] = str(date.today() - timedelta(days=20))
    res = client.put("/api/tenants/", json=valid_tenant_update_payload)
    assert res.status_code == 400


# ---------- DELETE ----------
@patch("tenants.repositories.CommandTenants.delete_tenant")
def test_delete_tenant(mock_delete, client):
    res = client.delete("/api/tenants/1")
    assert res.status_code == 204
    mock_delete.assert_called_once_with(1)
