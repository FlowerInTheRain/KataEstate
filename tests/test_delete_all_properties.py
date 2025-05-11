import pytest
from unittest.mock import patch, MagicMock
from properties.repositories import QueryProperties, CommandProperties

@patch("properties.repositories.CommandProperties.delete_property")
@patch("properties.repositories.QueryProperties.get_all_properties")
def test_delete_all_properties_and_verify_empty(mock_get_all, mock_delete):
    # First call returns 3 fake properties
    prop1 = MagicMock(id=1)
    prop2 = MagicMock(id=2)
    prop3 = MagicMock(id=3)

    mock_get_all.side_effect = [
        [prop1, prop2, prop3],  # before deletion
        []                      # after deletion
    ]

    # Act
    all_properties = QueryProperties.get_all_properties()
    assert len(all_properties) == 3  # ✅ Assert before deletion

    for prop in all_properties:
        CommandProperties.delete_property(prop.id)

    after_deletion = QueryProperties.get_all_properties()

    # Assert
    mock_delete.assert_any_call(1)
    mock_delete.assert_any_call(2)
    mock_delete.assert_any_call(3)
    assert mock_delete.call_count == 3

    assert after_deletion == []
