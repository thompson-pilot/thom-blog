from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from django.urls import reverse
from taggit.managers import TaggableManager


class ArticlePublishedManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(status=Article.Status.PUBLISHED)
		pass
	pass


class Article(models.Model):

	class Status(models.TextChoices):
		DRAFT = 'DF', 'Draft'
		PUBLISHED = 'PB', 'Published'

	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_articles')
	title = models.CharField(max_length=250)
	slug= models.SlugField(max_length=250, unique_for_date='publish')
	body = models.TextField()
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=2,
								choices=Status.choices,
								default=Status.DRAFT
							)

	objects = models.Manager() # The default manager
	publishedArticles = ArticlePublishedManager() # The custom manager
	tags = TaggableManager()

	class Meta:
		ordering = ['-publish']
		indexes = [
			models.Index(fields=['-publish']),
		]
		pass


	def __str__(self):
		return self.title
		pass

	def get_canonical_url(self):
		return reverse('blog:article_details',
						args=[
								self.publish.year,
								self.publish.month,
								self.publish.day,
								self.slug
								]
							)
		pass

	pass


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields=["created"]),
        ]
    
    def __str__(self):
        return f"Comment by {self.name} on {self.article}"
        pass
    
    pass
