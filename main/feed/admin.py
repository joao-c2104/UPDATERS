from django.contrib import admin
from .models import Article, ArticleViewLog, Category

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'publication_date')
    search_fields = ('title', 'content', 'author')
    list_filter = ('category', 'publication_date')

admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleViewLog)
admin.site.register(Category)