import pytest
from unittest.mock import patch, MagicMock
from properties.repositories.QueryProperties import get_all_properties

@pytest.mark.usefixtures("app_context")
@patch("properties.repositories.QueryProperties.session")
def test_should_get_all_mocked_properties(mock_session):
    fake_property = MagicMock()
    fake_property.id = 1
    fake_property.address = "101 rue des acquevilles, 92150, Suresnes"
    fake_property.type = "Residential"
    fake_property.status = "Vacant"
    fake_property.purchase_date = "2021-01-01"
    fake_property.price = 900000

    mock_session.query.return_value.all.return_value = [fake_property]

    result = get_all_properties()

    assert len(result) == 1
    assert result[0].address == fake_property.address
