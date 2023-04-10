from django.shortcuts import render, get_object_or_404
from .models import Article
from django.http import HttpResponse
from django.http import Http404
from django.urls import reverse


def list_of_articles(request):
	articles = Article.publishedArticles.all()
	# print(articles)

	# return HttpResponse("This is list of articles webpage...")
	return render(request, 'blog/list.html', {'articles': articles})
	pass


def article_details(request, id):
	try:
		article = get_object_or_404(Article, id=id, status=Article.Status.PUBLISHED)
	except Article.DoesNotExist:
		raise Http404("No article found.")

	return render(request, 'blog/detail.html', {'article': article})
	pass


