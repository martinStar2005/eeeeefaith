from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from django.contrib.contenttypes.fields import GenericRelation
from core.models import Comment
from hitcount.models import HitCountMixin, HitCount
from ckeditor.fields import RichTextField

class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("Category Name"), max_length=100),
        description=models.TextField(_("Description"), blank=True),
    )
    order = models.PositiveIntegerField(_("Order"), default=0)
    
    class Meta:
        verbose_name = _("FAQ Category")
        verbose_name_plural = _("FAQ Categories")
        ordering = ['order']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('faq:category', kwargs={'pk': self.pk})

class Question(TranslatableModel, HitCountMixin):
    translations = TranslatedFields(
        question=models.CharField(_("Question"), max_length=255),
        answer=RichTextField(_("Answer")),
        meta_description=models.CharField(_("Meta Description"), max_length=255, blank=True),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions', verbose_name=_("Category"))
    is_featured = models.BooleanField(_("Featured"), default=False)
    views = models.PositiveIntegerField(_("Views"), default=0)
    likes = models.PositiveIntegerField(_("Likes"), default=0)
    comments = GenericRelation(Comment)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                         related_query_name='hit_count_generic_relation')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ['category__order', 'id']
    
    def __str__(self):
        return self.question
    
    def get_absolute_url(self):
        return reverse('faq:detail', kwargs={'pk': self.pk})
    
    def increment_view_count(self):
        self.views += 1
        self.save(update_fields=['views'])