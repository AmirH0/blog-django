from django.contrib import admin

# Register your models here.
from .models import Comment, Post, Category, Tag

admin.site.register(Comment)
# admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "category", "show_tags", "status")

    def show_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all()) or "-"
