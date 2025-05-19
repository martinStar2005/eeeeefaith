from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from hitcount.views import HitCountDetailView
from .models import Category, Question
from core.forms import CommentForm
from core.utils import get_content_type_id

def faq_home(request):
    """FAQ home page displaying categories and featured questions"""
    categories = Category.objects.all()
    featured_questions = Question.objects.filter(is_featured=True)[:5]
    
    context = {
        'categories': categories,
        'featured_questions': featured_questions,
    }
    
    return render(request, 'faq/home.html', context)

def category_questions(request, pk):
    """Display questions for a specific category"""
    category = get_object_or_404(Category, pk=pk)
    questions = category.questions.all()
    
    # Pagination
    paginator = Paginator(questions, 10)  # 10 questions per page
    page = request.GET.get('page', 1)
    questions_list = paginator.get_page(page)
    
    context = {
        'category': category,
        'questions': questions_list,
    }
    
    return render(request, 'faq/category.html', context)

def question_detail(request, pk):
    """Detail page for a question"""
    question = get_object_or_404(Question, pk=pk)
    
    # Increment view count
    question.increment_view_count()
    
    # Get content type for this model
    content_type_id = get_content_type_id('question')
    
    # Comments
    comments = question.comments.filter(is_approved=True)
    comment_form = CommentForm()
    
    # Related questions (from same category)
    related_questions = Question.objects.filter(
        category=question.category
    ).exclude(id=question.id)[:5]
    
    context = {
        'question': question,
        'related_questions': related_questions,
        'comments': comments,
        'comment_form': comment_form,
        'content_type_id': content_type_id,
    }
    
    return render(request, 'faq/detail.html', context)

def faq_search(request):
    """Search questions and answers"""
    query = request.GET.get('q', '')
    results = []
    
    if query:
        results = Question.objects.filter(
            Q(translations__question__icontains=query) | 
            Q(translations__answer__icontains=query)
        )
        
        # Pagination
        paginator = Paginator(results, 10)  # 10 results per page
        page = request.GET.get('page', 1)
        results = paginator.get_page(page)
    
    context = {
        'query': query,
        'results': results,
    }
    
    return render(request, 'faq/search.html', context)