from .models import SiteSettings

def site_settings(request):
    """
    Context processor to add site settings to all templates
    """
    try:
        settings = SiteSettings.objects.first()
    except:
        settings = None
        
    return {
        'site_settings': settings
    }