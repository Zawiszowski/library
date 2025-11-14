from rest_framework.test import APIClient
import pytest


@pytest.fixture
def annonymus_client() -> APIClient:
    return APIClient()
