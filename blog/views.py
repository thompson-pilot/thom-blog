from django.shortcuts import render, get_object_or_404
from .models import Article, Comment
from django.http import HttpResponse
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm
from django.views.decorators.http import require_POST




def list_of_articles(request):
	articles = Article.publishedArticles.all()

	paginator = Paginator(articles, 3)
	page_number = request.GET.get('page', 1)

	try:
		articles = paginator.page(page_number)
	except EmptyPage:
		articles = paginator.page(paginator.num_pages)
	except PageNotAnInteger:
		articles = paginator.page(1)
	
	return render(request, 'blog/list.html', {'articles': articles})
	pass


def article_details(request, year, month, day, article):
	try:
		article = get_object_or_404(Article, status=Article.Status.PUBLISHED,
					slug=article,
					publish__year=year,
					publish__month=month,
					publish__day=day
				)

		# List of active comments for this article
		comments = article.comments.filter(active=True)

		# Form for users to write comment
		form = CommentForm()

	except Article.DoesNotExist:
		raise Http404("No article found.")

	return render(request, "blog/detail.html", {
		"article": article,
		"comments": comments,
		"form": form}
	)
	pass


@require_POST
def comment_for_article(request, article_id):

    # get the article by article_id
    article = get_object_or_404(Article, id = article_id, status=Article.Status.PUBLISHED)
    comment = None
    
    # A comment form
    
    # form = CommentForm(data=request.Article)
    form = CommentForm(data=request.POST)

    if form.is_valid():
        # Create a Comment object before saving it to the database
        comment = form.save(commit=False)

        # Assign the article to the comment
        comment.article = article
        # Save the comment to the database
        comment.save()
        pass

    return render(request, "blog/comment.html", {"article": article, "form": form, "comment": comment})

    pass










