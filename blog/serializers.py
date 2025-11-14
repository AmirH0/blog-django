from rest_framework import serializers
from .models import Post, Category, Tag
from django.utils.text import slugify


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()  
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source="comments.count", read_only=True)
    like_count = serializers.IntegerField(source="likes.count", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "author",
            "category",
            "tags",
            "excerpt",
            "body",
            "cover_image",
            "status",
            "published_at",
            "created_at",
            "updated_at",
            "comment_count",
            "like_count",
        ]

class PostCreateUpdateSerializer(serializers.ModelSerializer):

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True, required=False
    )
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, source="tags", write_only=True, required=False
    )

    class Meta:
        model = Post
        fields = ["title", "excerpt", "body", "cover_image", "status", "published_at", "category_id", "tag_ids"]

    def create(self, validated_data):
        tags = validated_data.pop("tags", [])
        post = Post.objects.create(**validated_data)
        if tags:
            post.tags.set(tags)
        post.slug = slugify(post.title)
        post.save()
        return post

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if tags is not None:
            instance.tags.set(tags)
        instance.slug = slugify(instance.title)
        instance.save()
        return instance