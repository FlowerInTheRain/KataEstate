# tests/test_update_property.py

import pytest
from unittest.mock import patch, MagicMock
from properties.repositories.CommandProperties import update_property
from properties.models.Properties import Property

@patch("properties.repositories.CommandProperties.session")
def test_should_update_property(mock_session):
    # Simulate an existing property in the DB
    existing = MagicMock(spec=Property)
    existing.id = 1

    # Patch session.get to return this fake object
    mock_session.get.return_value = existing

    # Create an updated property with new values
    updated = Property(
        id=1,
        address="3 rue Anna Coleman Ladd 93300 Aubervilliers",
        type="Residential",
        status="Vacant",
        purchase_date="2022-07-28",
        price=350000
    )

    # Act
    update_property(updated)

    # Captor-style assertions (verifying mutations)
    assert existing.address == updated.address
    assert existing.type == updated.type
    assert existing.status == updated.status
    assert existing.purchase_date == updated.purchase_date
    assert existing.price == updated.price

    # Ensure commit was called once
    mock_session.commit.assert_called_once()
