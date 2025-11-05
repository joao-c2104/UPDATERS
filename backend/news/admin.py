from django.contrib import admin
from .models import Article, Comment, Video, Poll


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_at")
    search_fields = ("title", "author")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "article", "created_at")
    search_fields = ("user", "text")
    list_filter = ("created_at",)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "article", "duration_seconds")
    search_fields = ("title", "description")


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ("question", "article", "votes")
    search_fields = ("question",)
