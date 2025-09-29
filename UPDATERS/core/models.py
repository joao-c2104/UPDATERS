from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# app: core/models.py
from django.db import models
from django.utils.text import slugify

class Visibility(models.TextChoices):
    DRAFT = "draft", "Rascunho"
    PUBLISHED = "published", "Publicado"
    ARCHIVED = "archived", "Arquivado"

class Topic(models.Model):
    """Tópicos (opcional, útil para filtrar/organizar)."""
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:100]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class NewsSummary(models.Model):
    """
    Resumo de notícia (texto curto). 
    Pode vir de fonte externa (source_url) ou ser curado internamente.
    """
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    tldr = models.CharField(max_length=300, help_text="Resumo direto ao ponto")
    body = models.TextField(blank=True, help_text="Opcional: versão um pouco maior")
    source_url = models.URLField(blank=True, help_text="Link da matéria original (se houver)")
    topics = models.ManyToManyField(Topic, blank=True, related_name="summaries")

    status = models.CharField(max_length=12, choices=Visibility.choices, default=Visibility.DRAFT)
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["status", "published_at"])]
        ordering = ["-published_at", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:200]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class VideoNews(models.Model):
    """
    Notícia em vídeo (formato short/reels).
    """
    title = models.CharField(max_length=160)
    file_url = models.URLField(help_text="URL do vídeo")
    caption = models.CharField(max_length=220, blank=True)
    duration_seconds = models.PositiveIntegerField(default=0)
    topics = models.ManyToManyField(Topic, blank=True, related_name="videos")

    status = models.CharField(max_length=12, choices=Visibility.choices, default=Visibility.DRAFT)
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

class SavedItem(models.Model):
    """
    Itens salvos pelo usuário para ler/assistir depois.
    Funciona para NewsSummary e VideoNews via ContentType.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="saved_items"
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    saved_at = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=140, blank=True, help_text="Opcional: anotação rápida")

    class Meta:
        indexes = [
            models.Index(fields=["user", "content_type", "object_id"]),
            models.Index(fields=["saved_at"]),
        ]
        unique_together = ("user", "content_type", "object_id")
        ordering = ["-saved_at"]

    def __str__(self):
        return f"{self.user} salvou {self.content_object} em {self.saved_at:%Y-%m-%d %H:%M}"
