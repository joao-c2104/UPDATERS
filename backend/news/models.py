from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True) 
    content = models.TextField()
    image = models.URLField(blank=True, null=True)
    author = models.CharField(max_length=120, blank=True)
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
