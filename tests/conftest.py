# file: tests/conftest.py

import pytest
from app.app import create_app  # Adjusted import statement

@pytest.fixture
def app():
    app = create_app({'TESTING': True})  # Enable testing mode
    with app.app_context():  # Push an application context
        yield app
