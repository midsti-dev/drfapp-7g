import pytest
from pytest_drf.util import url_for
from posts.models import Post
from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db


def test_post_list(api_client):
    url = url_for("posts-list")
    response = api_client.get(url)

    assert response.status_code == 200
    assert isinstance(response.data, list)


def test_post_create(api_client):
    user = User.objects.create_user(username="testuser", password="pass12345")

    api_client.force_authenticate(user=user)

    url = url_for("posts-list")

    payload = {
        "title": "My Test Post",
        "content": "Hello World",
        "author": user.id,
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == 201
    assert Post.objects.count() == 1
    assert response.data["title"] == "My Test Post"


def test_post_retrieve(api_client):
    user = User.objects.create_user(username="testuser", password="pass12345")
    post = Post.objects.create(title="Test", content="C", author=user)

    url = url_for("posts-detail", post.id)
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["id"] == post.id
    assert response.data["title"] == "Test"
