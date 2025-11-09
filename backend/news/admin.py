from django.contrib import admin
from .models import Article, Comment, Video, Poll


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author_name",
                    "published_at", "get_comments_count")
    search_fields = ("title", "author_name")
    fields = ("title", "summary", "content", "image", "author_name")

    def get_comments_count(self, obj):
        return obj.comments_count
    get_comments_count.short_description = "Comments"


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
