from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Book, Chapter, Verse
from core.utils import get_content_type_id

def bible_home(request):
    """Bible home page with all books"""
    books = Book.objects.all()
    featured_verses = Verse.objects.order_by('?')[:3]
    
    context = {
        'books': books,
        'featured_verses': featured_verses,
    }
    
    return render(request, 'bible/home.html', context)

def book_detail(request, pk):
    """Detail page for a book showing all chapters"""
    book = get_object_or_404(Book, pk=pk)
    chapters = book.chapters.all()
    
    context = {
        'book': book,
        'chapters': chapters,
    }
    
    return render(request, 'bible/book_detail.html', context)

def chapter_detail(request, book_id, chapter_num):
    """Detail page for a chapter showing all verses"""
    book = get_object_or_404(Book, pk=book_id)
    chapter = get_object_or_404(Chapter, book=book, number=chapter_num)
    verses = chapter.verses.all()
    
    # Navigation for previous and next chapter
    prev_chapter = Chapter.objects.filter(
        book=book, number__lt=chapter_num
    ).order_by('-number').first()
    
    next_chapter = Chapter.objects.filter(
        book=book, number__gt=chapter_num
    ).order_by('number').first()
    
    context = {
        'book': book,
        'chapter': chapter,
        'verses': verses,
        'prev_chapter': prev_chapter,
        'next_chapter': next_chapter,
    }
    
    return render(request, 'bible/chapter_detail.html', context)

def verse_detail(request, book_id, chapter_num, verse_num):
    """Detail page for a single verse"""
    book = get_object_or_404(Book, pk=book_id)
    chapter = get_object_or_404(Chapter, book=book, number=chapter_num)
    verse = get_object_or_404(Verse, chapter=chapter, number=verse_num)
    
    # Increment view count
    verse.increment_view_count()
    
    # Get content type for this model
    content_type_id = get_content_type_id('verse')
    
    context = {
        'book': book,
        'chapter': chapter,
        'verse': verse,
        'content_type_id': content_type_id,
    }
    
    return render(request, 'bible/verse_detail.html', context)

def bible_search(request):
    """Search the Bible"""
    query = request.GET.get('q', '')
    results = []
    
    if query:
        results = Verse.objects.filter(translations__text__icontains=query)
        
        # Pagination
        paginator = Paginator(results, 20)  # 20 verses per page
        page = request.GET.get('page', 1)
        results = paginator.get_page(page)
    
    context = {
        'query': query,
        'results': results,
    }
    
    return render(request, 'bible/search.html', context)