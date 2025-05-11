import pytest
from unittest.mock import patch, MagicMock
from properties.repositories.CommandProperties import create_property

@pytest.mark.usefixtures("app_context")
@patch("properties.repositories.CommandProperties.session")
def test_should_create_property( mock_session):
    # Arrange: build a fake input object
    mocked_properties = MagicMock()
    mocked_properties.address = "3, rue Anna Coleman Ladd 93300 Aubervilliers"
    mocked_properties.type.value = "Commercial"
    mocked_properties.status.value = "Occupied"
    mocked_properties.purchase_date = "2022-07-28"
    mocked_properties.price = 350000

    # Act
    create_property(mocked_properties)


    # Assert: object was added and committed to the session
    mock_session.add.assert_called_once()
    added_obj = mock_session.add.call_args[0][0]
    assert added_obj.address == mocked_properties.address
    mock_session.commit.assert_called_once()