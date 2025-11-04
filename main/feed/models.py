from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    
    # === CAMPO ADICIONADO ===
    # Adicionamos o autor, conforme os textos que você enviou.
    author = models.CharField(max_length=100, verbose_name="Autor")
    
    summary = models.TextField(verbose_name="Resumo")
    content = models.TextField(verbose_name="Conteúdo Completo")
    image = models.ImageField(upload_to='articles/', verbose_name="Imagem de Destaque")
    publication_date = models.DateTimeField(default=timezone.now, verbose_name="Data de Publicação")
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