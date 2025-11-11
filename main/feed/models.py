from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome da Categoria")
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['name']

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    author = models.CharField(max_length=100, verbose_name="Autor")
    summary = models.TextField(verbose_name="Resumo")
    content = models.TextField(verbose_name="Conteúdo Completo")
    image = models.ImageField(upload_to='articles/', verbose_name="Imagem de Destaque")
    publication_date = models.DateTimeField(default=timezone.now, verbose_name="Data de Publicação")
    view_count = models.PositiveIntegerField(default=0, verbose_name="Contagem de Visualizações")
    slug = models.SlugField(max_length=255, unique=True, blank=True, editable=False)

    class Meta:
        ordering = ['-publication_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'slug': self.slug})
    
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Categoria"
    )
    
class ArticleViewLog(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="view_logs")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Visualização em '{self.article.title}' em {self.timestamp.strftime('%d/%m/%Y')}"