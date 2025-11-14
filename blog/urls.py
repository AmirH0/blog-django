from django.urls import path
from .views import PostListCreateAPIView, PostRetriveUpdataDestroyApi

urlpatterns = [
    path("posts/", PostListCreateAPIView.as_view(), name="post-list"),
    path(
        "posts/<slug:slug>/",
        PostRetriveUpdataDestroyApi.as_view(),
        name="post-detail",
    ),
]
