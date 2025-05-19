from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class SiteSettings(models.Model):
    site_name = models.CharField(_("Site Name"), max_length=100, default="Martin Faith")
    tagline = models.CharField(_("Tagline"), max_length=255, default="Coming to Christian")
    logo = models.ImageField(_("Logo"), upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(_("Favicon"), upload_to='site/', blank=True, null=True)
    footer_text = models.TextField(_("Footer Text"), blank=True)
    facebook = models.URLField(_("Facebook"), blank=True)
    twitter = models.URLField(_("Twitter"), blank=True)
    instagram = models.URLField(_("Instagram"), blank=True)
    youtube = models.URLField(_("YouTube"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Site Settings")
        verbose_name_plural = _("Site Settings")
    
    def __str__(self):
        return self.site_name

class Comment(models.Model):
    # Generic relation to allow comments on any model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Comment data
    name = models.CharField(_("Name"), max_length=100)
    email = models.EmailField(_("Email"))
    content = models.TextField(_("Content"))
    is_approved = models.BooleanField(_("Approved"), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.name}"