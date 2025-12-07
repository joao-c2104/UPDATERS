from django.views.generic import ListView, DetailView, TemplateView
from .models import Article, ArticleViewLog, Comment
from django.db.models import Q, F
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json


class ArticleListView(ListView):
    model = Article
    template_name = 'feed/feed.html'
    context_object_name = 'articles'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().select_related('category') 
        
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

    def get_queryset(self):
        return super().get_queryset().select_related('category')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.view_count = F('view_count') + 1
        obj.save(update_fields=['view_count'])
        ArticleViewLog.objects.create(article=obj)
        obj.refresh_from_db()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        is_favorited = False
        if self.request.user.is_authenticated:
            is_favorited = article.favorites.filter(id=self.request.user.id).exists()
        context['is_favorited'] = is_favorited
        return context

class HomeView(TemplateView):
    template_name = 'feed/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_qs = Article.objects.select_related('category').order_by('-publication_date')
        
        hero_article = base_qs.first()
        
        if hero_article:
            grid_articles = base_qs.exclude(pk=hero_article.pk)[:4]
        else:
            grid_articles = base_qs[:4]

        context['hero_article'] = hero_article
        context['grid_articles'] = grid_articles

        return context

@login_required
def toggle_favorite_view(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if article.favorites.filter(id=request.user.id).exists():
        article.favorites.remove(request.user)
    else:
        article.favorites.add(request.user)

    return redirect('article-detail', slug=article.slug)

@login_required
def favorites_list_view(request):
    favorited_articles = request.user.favorite_articles.all()

    context = {
        'articles': favorited_articles
    }
    return render(request, 'feed/favorites.html', context)

@require_http_methods(["GET", "POST"])
def article_comments_api(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == "GET":
        comments = Comment.objects.filter(article=article).select_related('author')
        comments_data = [
            {
                'id': comment.id,
                'author': comment.author.username,
                'content': comment.content,
                'created_at': comment.created_at.strftime('%d/%m/%Y às %H:%M'),
                'is_owner': request.user == comment.author
            }
            for comment in comments
        ]
        return JsonResponse({
            'comments': comments_data,
            'count': len(comments_data)
        })

    elif request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Você precisa estar logado para comentar.'}, status=401)

        try:
            data = json.loads(request.body)
            content = data.get('content', '').strip()

            if not content:
                return JsonResponse({'error': 'O comentário não pode estar vazio.'}, status=400)

            if len(content) > 300:
                return JsonResponse({'error': 'O comentário não pode ter mais de 300 caracteres.'}, status=400)

            comment = Comment.objects.create(
                article=article,
                author=request.user,
                content=content
            )

            return JsonResponse({
                'success': True,
                'comment': {
                    'id': comment.id,
                    'author': comment.author.username,
                    'content': comment.content,
                    'created_at': comment.created_at.isoformat(),
                }
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dados inválidos.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Erro ao criar comentário.'}, status=500)

@require_http_methods(["GET"])
def article_comments_count_api(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    count = Comment.objects.filter(article=article).count()
    return JsonResponse({'count': count})