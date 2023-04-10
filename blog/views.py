from django.shortcuts import render
from .models import Article
from django.http import HttpResponse

def list_of_articles(request):
	articles = Article.publishedArticles.all()
	# print(articles)

	# return HttpResponse("This is list of articles webpage...")
	return render(request, 'blog/list.html', {'articles': articles})
	pass


