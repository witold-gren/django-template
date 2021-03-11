"""
Test for the utils app.
"""

from django.conf import settings
from django.urls import reverse

from rest_framework import status


def test_openapi_spec_endpoint(client):
    view_name = settings.OPENAPI_SCHEMA_VIEW_NAME
    url = reverse(view_name)
    response = client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, dict)
    assert "openapi" in response.data
