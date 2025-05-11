import pytest
from datetime import date, timedelta
from unittest.mock import patch, MagicMock

from properties.models.PropertyStatuses import PropertyStatuses
from properties.models.PropertyTypes import PropertyTypes


@pytest.fixture
def valid_property_payload():
    return {
        "address": "123 Main Street",
        "type": PropertyTypes.RESIDENTIAL.value,
        "status": PropertyStatuses.VACANT.value,
        "purchase_date": str(date.today() - timedelta(days=1)),
        "price": 250000
    }

@pytest.mark.usefixtures("app_context")
@patch("properties.repositories.CommandProperties.create_property")
def test_post_property_creates_property(mock_create, client, valid_property_payload):
    res = client.post("/api/properties/", json=valid_property_payload)
    assert res.status_code == 204
    mock_create.assert_called_once()


@patch("properties.repositories.QueryProperties.get_all_properties")
def test_get_properties_returns_list(mock_get, client):
    mock_get.return_value = [
        MagicMock(id=1, address="123 Main Street", type="Residential", status="Vacant", purchase_date="2021-01-01", price=100000)
    ]
    res = client.get("/api/properties/")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["address"] == "123 Main Street"


@patch("properties.repositories.CommandProperties.update_property")
def test_put_property_updates(mock_update, client, valid_property_payload):
    updated_payload = valid_property_payload.copy()
    updated_payload.update({
        "id": 1,
        "address": "456 Updated Street"
    })

    res = client.put("/api/properties/", json=updated_payload)
    assert res.status_code == 204
    mock_update.assert_called_once()


@patch("properties.repositories.CommandProperties.delete_property")
def test_delete_property(mock_delete, client):
    res = client.delete("/api/properties/1")
    assert res.status_code == 204
    mock_delete.assert_called_once_with(1)
