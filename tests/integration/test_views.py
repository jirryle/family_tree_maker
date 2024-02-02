# file: tests/integration/test_views.py

import pytest
from flask import url_for

@pytest.mark.usefixtures('client')  # Use the client fixture provided by pytest-flask
class TestViews:
    def test_index_page(self, client):
        """
        GIVEN a Flask application
        WHEN the index page is requested (GET)
        THEN check the response is valid and the correct page is returned
        """
        response = client.get(url_for('index'))
        assert response.status_code == 200