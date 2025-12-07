from django.core.cache import cache
from .models import Article, ArticleViewLog, Category
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count


def trending_articles_processor(request):
    trending_articles = cache.get('trending_articles')

    if not trending_articles:
        one_month_ago = timezone.now() - timedelta(days=30)
        
        top_articles_data = ArticleViewLog.objects.filter(
            timestamp__gte=one_month_ago
        ).values('article_id').annotate(
            recent_views=Count('article_id')
        ).order_by('-recent_views')[:5]

        top_article_ids = [item['article_id'] for item in top_articles_data]

        articles_qs = Article.objects.filter(pk__in=top_article_ids).select_related('category')
        articles_dict = {a.id: a for a in articles_qs}
        trending_articles = [articles_dict[id] for id in top_article_ids if id in articles_dict]

        cache.set('trending_articles', trending_articles, 900)

    return {'trending_articles': trending_articles}

def all_categories_processor(request):
    categories = cache.get('all_categories')
    if not categories:
        categories = list(Category.objects.all())
        cache.set('all_categories', categories, 3600)
    
    return {'all_categories': categories}