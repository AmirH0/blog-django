from django.urls import path
from .views import PostListCreateAPIView, PostRetriveUpdataDestroyApi, CommentAPIView , CommentDetailApiView

urlpatterns = [
    path("posts/", PostListCreateAPIView.as_view(), name="post-list"),
    path(
        "posts/<slug:slug>/",
        PostRetriveUpdataDestroyApi.as_view(),
        name="post-detail",
    ),
    path("posts/<int:post_id>/comments/", CommentAPIView.as_view(), name="comments"),
    path("comments/<int:comment_id>/", CommentDetailApiView.as_view(), name="comment-detail"),
]
