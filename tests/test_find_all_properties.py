import pytest
from unittest.mock import patch, MagicMock
from properties.repositories.QueryProperties import get_all_properties

from properties.models.Properties import Property


@pytest.mark.usefixtures("app_context")
@patch("properties.repositories.QueryProperties.session")
def test_should_get_all_properties_returns_mocked_results(mock_session):
    fake_property = Property()
    fake_property.id = 1
    fake_property.address = "101 rue des acquevilles, 92150, Suresnes"
    fake_property.type = "Residential"
    fake_property.status = "Vacant"
    fake_property.purchase_date = "2021-01-01"
    fake_property.price = 900000

    mock_query = MagicMock()
    mock_query.order_by.return_value.all.return_value = [fake_property]
    mock_session.query.return_value = mock_query

    result = get_all_properties()

    assert len(result) == 1
    assert result[0].address == fake_property.address
