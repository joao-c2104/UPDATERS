from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article
from django.db.models import Q

class ArticleListView(ListView):
    model = Article
    template_name = 'feed/feed.html'
    context_object_name = 'articles'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset() 
        query = self.request.GET.get('q') 

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            ).distinct()
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