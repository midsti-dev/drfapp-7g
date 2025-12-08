import pytest
from pytest_drf.util import url_for
from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db


def test_user_list(api_client):
    url = url_for("users-list")
    response = api_client.get(url)

    assert response.status_code == 200
    assert isinstance(response.data, list)


def test_user_create(api_client):
    url = url_for("users-list")

    payload = {
        "username": "john",
        "password": "pass12345"
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == 201
    assert User.objects.count() == 1
    assert response.data["username"] == "john"


def test_user_retrieve(api_client):
    user = User.objects.create_user(username="bob", password="pass123")

    url = url_for("users-detail", user.id)
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["id"] == user.id
    assert response.data["username"] == "bob"
