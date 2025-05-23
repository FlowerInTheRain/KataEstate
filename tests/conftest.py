import os

import pytest

from app.app import create_app
from db import Base, engine


@pytest.fixture(scope="session")
def app_context():
    api = create_app(testing=True)
    with api.app_context():
        # Crée les tables avant tout
        Base.metadata.create_all(bind=engine)
        yield
        # Nettoie après tous les tests


@pytest.fixture
def client(app_context):
    app = create_app(testing=True)
    return app.test_client()
