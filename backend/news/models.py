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


class Comment(models.Model):
    user = models.CharField(max_length=120)
    text = models.TextField(max_length=500)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.article.title}"


class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_url = models.URLField()
    duration_seconds = models.IntegerField()
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='videos')

    def __str__(self):
        return self.title


class Poll(models.Model):
    question = models.CharField(max_length=200)
    options = models.JSONField()
    votes = models.IntegerField(default=0)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='polls')

    def __str__(self):
        return self.question
