from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.utils.text import slugify

def get_content_type_id(model_name):
    """Get content type ID from model name"""
    try:
        return ContentType.objects.get(model=model_name.lower()).id
    except ContentType.DoesNotExist:
        return None

def unique_slug_generator(instance, new_slug=None):
    """Generate a unique slug for a model instance"""
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    
    if qs_exists:
        new_slug = f"{slug}-{Klass.objects.filter(slug__startswith=slug).count()}"
        return unique_slug_generator(instance, new_slug=new_slug)
    
    return slug