"""
URL configuration for martin_faith project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rosetta/', include('rosetta.urls')),  # Translation interface
    path('i18n/', include('django.conf.urls.i18n')),  # Language switching
]

# Translatable URLs
urlpatterns += i18n_patterns(
    path('', include('core.urls')),
    path('news/', include('news.urls')),
    path('bible/', include('bible.urls')),
    path('faq/', include('faq.urls')),
    path('testimonials/', include('testimonials.urls')),
    path('about/', include('about.urls')),
    prefix_default_language=False,
)

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)