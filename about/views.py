from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import About

def about(request):
    """About page"""
    try:
        about_info = About.objects.first()
    except:
        about_info = None
    
    context = {
        'about': about_info,
    }
    
    return render(request, 'about/index.html', context)

def contact(request):
    """Contact page"""
    try:
        about_info = About.objects.first()
    except:
        about_info = None
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        if name and email and message:
            # Here you would normally process the contact form
            # For now we'll just show a success message
            messages.success(request, _("Your message has been sent successfully. We will get back to you soon!"))
            return redirect('about:contact')
        else:
            messages.error(request, _("Please fill in all fields."))
    
    context = {
        'about': about_info,
    }
    
    return render(request, 'about/contact.html', context)