from django.contrib import admin
from .models import (
    Category,
    Article,
    ArticleViewLog,
    Comment,
    FlashVideo,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_date",
                    "view_count", "category")
    list_filter = ("category", "publication_date")
    search_fields = ("title", "summary", "content", "author")
    readonly_fields = ('slug', 'view_count')
    date_hierarchy = "publication_date"


@admin.register(ArticleViewLog)
class ArticleViewLogAdmin(admin.ModelAdmin):
    list_display = ("article", "timestamp")
    list_filter = ("timestamp",)
    date_hierarchy = "timestamp"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "article", "created_at")
    list_filter = ("created_at",)
    search_fields = ("author__username", "content")
    date_hierarchy = "created_at"


@admin.register(FlashVideo)
class FlashVideoAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("title", "description")
    readonly_fields = ("created_at",)
