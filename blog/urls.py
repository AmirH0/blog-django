from django.urls import path
from .views import (
    PostListCreateAPIView,
    PostRetriveUpdataDestroyApi,
    CommentAPIView,
    CommentDetailApiView,
    categoryListCreateApi,
    TagListCreateAPIView,
)

urlpatterns = [
    path("posts/", PostListCreateAPIView.as_view(), name="post-list"),
    path(
        "posts/<slug:slug>/",
        PostRetriveUpdataDestroyApi.as_view(),
        name="post-detail",
    ),
    path("posts/<int:post_id>/comments/", CommentAPIView.as_view(), name="comments"),
    path(
        "comments/<int:comment_id>/",
        CommentDetailApiView.as_view(),
        name="comment-detail",
    ),
    path("categories/", categoryListCreateApi.as_view()),
    path("tags/", TagListCreateAPIView.as_view()),
]
