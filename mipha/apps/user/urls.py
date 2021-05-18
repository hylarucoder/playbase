from django.conf import settings
from django.urls import path, include

from rest_framework import routers
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)

from mipha.apps.user.views import APIRootView
from mipha.apps.user.views.blog import BlogPostAPIView, BlogPostListAPIView, BlogPostArchiveAPIView, \
    BlogCategoryAPIView, BlogTagsAPIView
from mipha.apps.user.views.search import BlogSearchAPIView

router = routers.DefaultRouter()

urlpatterns = [
    path(
        r"v1/auth/api-auth", include("rest_framework.urls", namespace="rest_framework")
    ),
    path(r"v1/auth/api-token-auth", obtain_jwt_token),
    path(r"v1/auth/api-token-refresh", refresh_jwt_token),
    path(r"v1/auth/api-token-verify", verify_jwt_token),
    path(r"v1/blog-post/<str:title>", BlogPostAPIView.as_view()),
    path(r"v1/blog-posts", BlogPostListAPIView.as_view()),
    path(r"v1/blog-posts/search", BlogSearchAPIView.as_view()),
    path(r"v1/archive", BlogPostArchiveAPIView.as_view()),
    path(r"v1/category", BlogCategoryAPIView.as_view()),
    path(r"v1/tags", BlogTagsAPIView.as_view()),
    path(r"^", include(router.urls)),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(r"all", APIRootView.as_view(), name="all_api"),
    ]
