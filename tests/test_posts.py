from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from posts.models import Post


class PostsAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="pass12345"
        )

        # Создаем пост
        self.post = Post.objects.create(
            title="Test post",
            content="Some content",
            author=self.user
        )
        self.list_url = reverse("posts-list")

        self.detail_url = reverse("posts-detail", args=[self.post.id])


        self.client.force_authenticate(user=self.user)

    def test_get_posts_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_post(self):

        data = {
            "title": "New Post",
            "content": "Hello!",
            "author": self.user.id
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_get_single_post(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.post.title)

    def test_update_post(self):
        data = {
            "title": "Updated title",
            "content": "Updated content",
            "author": self.user.id
        }
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated title")

    def test_delete_post(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())
