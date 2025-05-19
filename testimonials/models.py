from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from django.contrib.contenttypes.fields import GenericRelation
from core.models import Comment
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save
from django.dispatch import receiver
from core.utils import unique_slug_generator

class Testimony(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(_("Title"), max_length=200),
        content=RichTextField(_("Content")),
    )
    slug = models.SlugField(_("Slug"), max_length=255, unique=True)
    author = models.CharField(_("Author Name"), max_length=100)
    email = models.EmailField(_("Email"), blank=True)
    author_image = models.ImageField(_("Author Image"), upload_to='testimonials/', blank=True, null=True)
    is_approved = models.BooleanField(_("Approved"), default=False)
    is_featured = models.BooleanField(_("Featured"), default=False)
    views = models.PositiveIntegerField(_("Views"), default=0)
    likes = models.PositiveIntegerField(_("Likes"), default=0)
    comments = GenericRelation(Comment)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Testimony")
        verbose_name_plural = _("Testimonies")
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('testimonials:detail', kwargs={'slug': self.slug})
    
    def increment_view_count(self):
        self.views += 1
        self.save(update_fields=['views'])

@receiver(pre_save, sender=Testimony)
def set_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)