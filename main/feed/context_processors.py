from .models import Article, ArticleViewLog, Category
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

def trending_articles_processor(request):
    one_month_ago = timezone.now() - timedelta(days=30)
    recent_view_logs = ArticleViewLog.objects.filter(
        timestamp__gte=one_month_ago
    )

    top_articles_data = recent_view_logs.values('article_id') \
                                        .annotate(recent_views=Count('article_id')) \
                                        .order_by('-recent_views')[:3]

    top_article_ids = [item['article_id'] for item in top_articles_data]
    trending_articles = list(Article.objects.filter(pk__in=top_article_ids))

    try:
        trending_articles.sort(key=lambda x: top_article_ids.index(x.id))
    except ValueError:
        pass

    return {'trending_articles': trending_articles}

def all_categories_processor(request):
    categories = Category.objects.all()
    return {'all_categories': categories}