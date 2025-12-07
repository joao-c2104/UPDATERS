from django.contrib import admin
from .models import Article, ArticleViewLog, Category, Comment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'publication_date')
    search_fields = ('title', 'content', 'author')
    list_filter = ('category', 'publication_date')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'article', 'content', 'created_at')
    search_fields = ('content', 'author__username', 'article__title')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)

admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleViewLog)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)