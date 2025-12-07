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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        is_favorited = False

        if self.request.user.is_authenticated:
            is_favorited = article.favorites.filter(
                id=self.request.user.id).exists()

        context['is_favorited'] = is_favorited
        return context


class HomeView(TemplateView):
    template_name = 'feed/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        hero_article = Article.objects.order_by('-publication_date').first()
        grid_articles = Article.objects.order_by('-publication_date').all()

        if hero_article:
            grid_articles = grid_articles.exclude(pk=hero_article.pk)[0:4]
        else:
            grid_articles = grid_articles[0:4]

        context['hero_article'] = hero_article
        context['grid_articles'] = grid_articles

        return context


@login_required
def toggle_favorite_view(request, article_id):
    """Toggle favorite and redirect back to article detail"""
    article = get_object_or_404(Article, id=article_id)

    if article.favorites.filter(id=request.user.id).exists():
        article.favorites.remove(request.user)
    else:
        article.favorites.add(request.user)

    return redirect('article-detail', slug=article.slug)


@login_required
@require_http_methods(["POST"])
def toggle_favorite_redirect_to_saved(request, article_id):
    """Toggle favorite and redirect to saved page (for article detail page)"""
    article = get_object_or_404(Article, id=article_id)

    if article.favorites.filter(id=request.user.id).exists():
        article.favorites.remove(request.user)
    else:
        article.favorites.add(request.user)

    return redirect('favorites_list')


@login_required
@require_http_methods(["POST"])
def toggle_favorite_api(request, article_id):
    """AJAX API endpoint for toggling favorites"""
    article = get_object_or_404(Article, id=article_id)

    is_favorited = article.favorites.filter(id=request.user.id).exists()

    if is_favorited:
        article.favorites.remove(request.user)
        is_favorited = False
    else:
        article.favorites.add(request.user)
        is_favorited = True

    return JsonResponse({
        'success': True,
        'is_favorited': is_favorited,
        'favorites_count': article.favorites.count()
    })


@login_required
def favorites_list_view(request):
    favorited_articles = request.user.favorite_articles.all()

    context = {
        'articles': favorited_articles
    }
    return render(request, 'feed/favorites.html', context)


@login_required
def saved_articles(request):
    """View to display all saved articles for the current user"""
    articles = request.user.favorite_articles.all()

    context = {
        'articles': articles
    }
    return render(request, 'feed/saved_articles.html', context)


@login_required
@require_http_methods(["POST"])
def toggle_save_article(request, slug):
    """Toggle save/unsave an article by slug"""
    article = get_object_or_404(Article, slug=slug)

    # Toggle the saved state
    if request.user in article.favorites.all():
        article.favorites.remove(request.user)
    else:
        article.favorites.add(request.user)

    # Check if we should redirect to saved page
    redirect_to_saved = request.GET.get('redirect') == 'saved'

    if redirect_to_saved:
        return redirect('saved_articles')
    else:
        # Redirect back to where the user came from
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        else:
            return redirect('article-list')

# Comment API Views


@require_http_methods(["GET", "POST"])
def article_comments_api(request, article_id):
    """
    GET: List all comments for an article
    POST: Create a new comment for an article
    """
    article = get_object_or_404(Article, id=article_id)

    if request.method == "GET":
        comments = Comment.objects.filter(
            article=article).select_related('author')
        comments_data = [
            {
                'id': comment.id,
                'author': comment.author.username,
                'content': comment.content,
                'created_at': comment.created_at.isoformat(),
            }
            for comment in comments
        ]
        return JsonResponse({
            'comments': comments_data,
            'count': len(comments_data)
        })

    elif request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({
                'error': 'Você precisa estar logado para comentar.'
            }, status=401)

        try:
            data = json.loads(request.body)
            content = data.get('content', '').strip()

            # Validation
            if not content:
                return JsonResponse({
                    'error': 'O comentário não pode estar vazio.'
                }, status=400)

            if len(content) > 300:
                return JsonResponse({
                    'error': 'O comentário não pode ter mais de 300 caracteres.'
                }, status=400)

            # Create comment
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
            return JsonResponse({
                'error': 'Dados inválidos.'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'error': 'Erro ao criar comentário.'
            }, status=500)


@require_http_methods(["GET"])
def article_comments_count_api(request, article_id):
    """
    GET: Get the comment count for an article
    """
    article = get_object_or_404(Article, id=article_id)
    count = Comment.objects.filter(article=article).count()
    return JsonResponse({'count': count})
