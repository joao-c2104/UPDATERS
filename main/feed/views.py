from django.views.generic import ListView, DetailView
from .models import Article, ArticleViewLog
from django.db.models import Q, F

class ArticleListView(ListView):
    model = Article
    template_name = 'feed/feed.html'
    context_object_name = 'articles'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset() 
        query = self.request.GET.get('q')
        category_id = self.request.GET.get('category')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            ).distinct()

        if category_id:
            queryset = queryset.filter(category__id=category_id)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')

        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'feed/article_detail.html'
    context_object_name = 'article'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.view_count = F('view_count') + 1
        obj.save(update_fields=['view_count'])

        ArticleViewLog.objects.create(article=obj)
        obj.refresh_from_db()
        
        return obj