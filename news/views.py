from django.shortcuts import render, get_object_or_404
from news.models import Article

def news_list(request):
    articles = Article.objects.order_by('-published_at')
    context = {'articles': articles}
    return render(request, 'news/news.html', context)

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    context = {'article': article}
    return render(request, 'news/detail.html', context) 
