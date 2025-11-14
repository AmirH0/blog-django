from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Post
from .serializers import PostSerializer, PostCreateUpdateSerializer


class PostListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        posts = (
            Post.objects.filter(status="published")
            .select_related("author", "category")
            .prefetch_related("tags")
        )
        serializer = PostSerializer(posts, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PostCreateUpdateSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            post = serializer.save(author=request.user)
            return Response(
                PostSerializer(post, context={"request": request}).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostRetriveUpdataDestroyApi(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, slug):
        return get_object_or_404(Post, slug=slug)

    def get(self, request, slug):
        post = self.get_object(slug)
        seriailizer = PostSerializer(post, context={"request": request})
        return Response(seriailizer.data)

    def put(self, request, slug):
        post = self.get_object(slug)
        if request.user != post.author and not request.user.is_staff:
            return Response(
                {"detail": "you not have permmion"}, status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = PostCreateUpdateSerializer(post, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response(PostSerializer(post, context={"request": request}).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        post = self.get_object(slug)
        if request.user != post.author and not request.user.is_staff:
            return Response(
                {"detail": "You don't have permission."},
                status=status.HTTP_403_FORBIDDEN,
            )
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
