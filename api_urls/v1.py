from django.urls import path, include
from rest_framework.routers import DefaultRouter

from posts.views import PostsViewSet
from users.views import UserViewSet

router = DefaultRouter()
router.register(r"posts", PostsViewSet, basename="posts")
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
]