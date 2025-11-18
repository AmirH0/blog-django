from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Category, Tag
from .serializers import (
    PostSerializer,
    PostCreateUpdateSerializer,
    CommentSerializer,
    CategorySerializer,
    TagSerializer,
)


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


class CommentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, post_id):
        comments = Comment.objects.filter(post_id=post_id, parent__isnull=True)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, post_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post_id=post_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, comment_id):
        try:
            return Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return None

    def put(self, request, comment_id):
        comment = self.get_object(comment_id)

        if not comment:
            return Response({"detail": "not found"}, status=status.HTTP_404_NOT_FOUND)

        if comment.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error_messages)

    def delete(self, request, comment_id):
        comment = self.get_object(comment_id)
        if not comment:
            return Response(
                {"detail:": "not fpund id is wrong"}, status=status.HTTP_404_NOT_FOUND
            )

        if comment.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response(status=status.HTTP_200_OK)


class categoryListCreateApi(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        category = Category.objects.all()
        seriilzer = CategorySerializer(category, many=True)
        return Response(seriilzer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class TagListCreateAPIView(APIView):
    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
