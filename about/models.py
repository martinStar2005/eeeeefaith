from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from ckeditor.fields import RichTextField

class About(TranslatableModel):
    translations = TranslatedFields(
        bio=RichTextField(_("Biography")),
        mission=models.TextField(_("Mission Statement"), blank=True),
        meta_description=models.CharField(_("Meta Description"), max_length=255, blank=True),
    )
    name = models.CharField(_("Name"), max_length=100)
    profile_image = models.ImageField(_("Profile Image"), upload_to='about/')
    email = models.EmailField(_("Email"))
    phone = models.CharField(_("Phone"), max_length=20, blank=True)
    facebook = models.URLField(_("Facebook"), blank=True)
    twitter = models.URLField(_("Twitter"), blank=True)
    instagram = models.URLField(_("Instagram"), blank=True)
    youtube = models.URLField(_("YouTube"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("About")
        verbose_name_plural = _("About")
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('about:index')