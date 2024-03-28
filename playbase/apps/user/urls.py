from django.conf import settings
from django.urls import path, include

# from playbase.apps.user.views import APIRootView
# from playbase.apps.user.views.blog import (
#     BlogPostAPIView,
#     BlogPostListAPIView,
#     BlogPostArchiveAPIView,
#     BlogCategoryAPIView,
#     BlogTagsAPIView,
# )
# from playbase.apps.user.views.search import BlogSearchAPIView

urlpatterns = [
    # path(
    #     r"v1/auth/api-auth", include("rest_framework.urls", namespace="rest_framework")
    # ),
    # path(r"v1/blog-post/<str:title>", BlogPostAPIView.as_view()),
    # path(r"v1/blog-posts", BlogPostListAPIView.as_view()),
    # path(r"v1/blog-posts/search", BlogSearchAPIView.as_view()),
    # path(r"v1/archive", BlogPostArchiveAPIView.as_view()),
    # path(r"v1/category", BlogCategoryAPIView.as_view()),
    # path(r"v1/tags", BlogTagsAPIView.as_view()),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        # path(r"all", APIRootView.as_view(), name="all_api"),
    ]
