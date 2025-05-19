from django import forms
from django.utils.translation import gettext_lazy as _
from parler.forms import TranslatableModelForm
from .models import Testimony
from ckeditor.widgets import CKEditorWidget

class TestimonyForm(TranslatableModelForm):
    class Meta:
        model = Testimony
        fields = ['author', 'email', 'title', 'content', 'author_image']
        widgets = {
            'content': CKEditorWidget(),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }