from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from .models import News, Category
from core.forms import CommentForm
from core.utils import get_content_type_id

def news_list(request):
    """Display all news articles"""
    all_news = News.objects.all()
    categories = Category.objects.all()
    
    # Pagination
    paginator = Paginator(all_news, 9)  # 9 news per page
    page = request.GET.get('page', 1)
    news_list = paginator.get_page(page)
    
    context = {
        'news_list': news_list,
        'categories': categories,
    }
    
    return render(request, 'news/list.html', context)

def category_news(request, pk):
    """Display news for a specific category"""
    category = get_object_or_404(Category, pk=pk)
    news_list = News.objects.filter(category=category)
    categories = Category.objects.all()
    
    # Pagination
    paginator = Paginator(news_list, 9)  # 9 news per page
    page = request.GET.get('page', 1)
    news_list = paginator.get_page(page)
    
    context = {
        'category': category,
        'news_list': news_list,
        'categories': categories,
    }
    
    return render(request, 'news/category.html', context)

def news_detail(request, slug):
    """Display a specific news article"""
    news = get_object_or_404(News, slug=slug)
    
    # Increment view count
    news.increment_view_count()
    
    # Related news (from same category)
    related_news = News.objects.filter(category=news.category).exclude(id=news.id)[:3]
    
    # Comments
    comments = news.comments.filter(is_approved=True)
    comment_form = CommentForm()
    
    # Get content type for this model
    content_type_id = get_content_type_id('news')
    
    context = {
        'news': news,
        'related_news': related_news,
        'comments': comments,
        'comment_form': comment_form,
        'content_type_id': content_type_id,
    }
    
    return render(request, 'news/detail.html', context)