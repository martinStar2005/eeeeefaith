from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_POST
from django.db.models import F, Count

from news.models import News
from bible.models import Verse
from faq.models import Question
from testimonials.models import Testimony

from .forms import EmailLoginForm, CommentForm
from .models import Comment


def home(request):
    """Home page view"""
    # Get latest content from each section
    latest_news = News.objects.order_by('-created_at')[:3]
    featured_verses = Verse.objects.order_by('?')[:3]
    popular_questions = Question.objects.annotate(view_count=Count('views')).order_by('-view_count')[:3]
    recent_testimonies = Testimony.objects.order_by('-created_at')[:3]

    context = {
        'latest_news': latest_news,
        'featured_verses': featured_verses,
        'popular_questions': popular_questions,
        'recent_testimonies': recent_testimonies,
    }

    return render(request, 'core/home.html', context)


def email_login(request):
    """Simple login with email only"""
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            login(request, user)
            messages.success(request, _("You have been logged in successfully."))
            return redirect('core:home')
    else:
        form = EmailLoginForm()

    return render(request, 'core/login.html', {'form': form})


def user_logout(request):
    """Log out user"""
    logout(request)
    messages.success(request, _("You have been logged out successfully."))
    return redirect('core:home')



def change_language(request):
    """Change the language preference"""
    lang = request.GET.get('lang', 'en')
    if lang in ['en', 'sv', 'fa']:
        # Set language in session
        request.session[translation.LANGUAGE_SESSION_KEY] = lang
        # Activate the language
        translation.activate(lang)
        # Set language cookie
        response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
        return response
    return HttpResponseRedirect('/')


@require_POST
def like_object(request, content_type, object_id):
    """Like/Unlike an object (news, testimony, etc.)"""
    # Get the content type
    ct = get_object_or_404(ContentType, id=content_type)
    # Get the object
    obj = get_object_or_404(ct.model_class(), id=object_id)

    # Check if user has already liked
    liked = request.session.get(f'liked_{content_type}_{object_id}', False)

    # Toggle like status
    if hasattr(obj, 'likes'):
        if liked:
            # Unlike
            obj.likes = F('likes') - 1
            request.session[f'liked_{content_type}_{object_id}'] = False
            message = _("You have unliked this.")
        else:
            # Like
            obj.likes = F('likes') + 1
            request.session[f'liked_{content_type}_{object_id}'] = True
            message = _("Thank you for your like!")

        obj.save(update_fields=['likes'])
        obj.refresh_from_db()  # Refresh to get the actual likes count

        return JsonResponse({
            'success': True,
            'message': message,
            'likes': obj.likes,
            'liked': not liked  # Return new like status
        })

    return JsonResponse({
        'success': False,
        'message': _("Object cannot be liked.")
    })


@require_POST
def add_comment(request, content_type, object_id):
    """Add a comment to any content type"""
    # Get the content type
    ct = get_object_or_404(ContentType, id=content_type)
    # Get the object
    obj = get_object_or_404(ct.model_class(), id=object_id)

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.content_type = ct
        comment.object_id = object_id
        comment.save()

        messages.success(request, _("Your comment has been submitted and is awaiting approval."))
    else:
        messages.error(request, _("There was an error with your comment. Please try again."))

    # Redirect back to the object's detail page
    if hasattr(obj, 'get_absolute_url'):
        return redirect(obj.get_absolute_url())
    else:
        return redirect('core:home')