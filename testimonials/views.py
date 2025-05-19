from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.translation import gettext as _
from .models import Testimony
from .forms import TestimonyForm
from core.forms import CommentForm
from core.utils import get_content_type_id

def testimony_list(request):
    """Display all approved testimonies"""
    testimonies = Testimony.objects.filter(is_approved=True)
    
    # Pagination
    paginator = Paginator(testimonies, 9)  # 9 testimonies per page
    page = request.GET.get('page', 1)
    testimony_list = paginator.get_page(page)
    
    context = {
        'testimony_list': testimony_list,
    }
    
    return render(request, 'testimonials/list.html', context)

def testimony_detail(request, slug):
    """Display a specific testimony"""
    testimony = get_object_or_404(Testimony, slug=slug, is_approved=True)
    
    # Increment view count
    testimony.increment_view_count()
    
    # Get content type for this model
    content_type_id = get_content_type_id('testimony')
    
    # Comments
    comments = testimony.comments.filter(is_approved=True)
    comment_form = CommentForm()
    
    # Related testimonies
    related_testimonies = Testimony.objects.filter(
        is_approved=True
    ).exclude(id=testimony.id).order_by('-created_at')[:3]
    
    context = {
        'testimony': testimony,
        'related_testimonies': related_testimonies,
        'comments': comments,
        'comment_form': comment_form,
        'content_type_id': content_type_id,
    }
    
    return render(request, 'testimonials/detail.html', context)

def submit_testimony(request):
    """Form for users to submit their testimonies"""
    if request.method == 'POST':
        form = TestimonyForm(request.POST, request.FILES)
        if form.is_valid():
            testimony = form.save(commit=False)
            testimony.is_approved = False  # All submissions need approval
            testimony.save()
            messages.success(request, _("Your testimony has been submitted and is awaiting approval. Thank you for sharing your story!"))
            return redirect('testimonials:list')
    else:
        form = TestimonyForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'testimonials/submit.html', context)

def featured_testimonies(request):
    """Display featured testimonies"""
    testimonies = Testimony.objects.filter(is_approved=True, is_featured=True)
    
    context = {
        'featured_testimonies': testimonies,
    }
    
    return render(request, 'testimonials/featured.html', context)