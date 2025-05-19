from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from django.contrib.contenttypes.fields import GenericRelation
from core.models import Comment
from ckeditor.fields import RichTextField
from core.utils import unique_slug_generator
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("Category Name"), max_length=100),
        description=models.TextField(_("Description"), blank=True),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('news:category', kwargs={'pk': self.pk})

class News(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(_("Title"), max_length=200),
        content=RichTextField(_("Content")),
        meta_description=models.CharField(_("Meta Description"), max_length=255, blank=True),
        meta_keywords=models.CharField(_("Meta Keywords"), max_length=255, blank=True),
    )
    slug = models.SlugField(_("Slug"), max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='news', verbose_name=_("Category"))
    featured_image = models.ImageField(_("Featured Image"), upload_to='news/')
    is_featured = models.BooleanField(_("Featured"), default=False)
    views = models.PositiveIntegerField(_("Views"), default=0)
    likes = models.PositiveIntegerField(_("Likes"), default=0)
    comments = GenericRelation(Comment)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'slug': self.slug})
    
    def increment_view_count(self):
        self.views += 1
        self.save(update_fields=['views'])

@receiver(pre_save, sender=News)
def set_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)