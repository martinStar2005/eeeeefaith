from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Category, Question

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ('name', 'order')
    search_fields = ('translations__name',)
    ordering = ('order',)

@admin.register(Question)
class QuestionAdmin(TranslatableAdmin):
    list_display = ('question', 'category', 'views', 'likes')
    list_filter = ('category',)
    search_fields = ('translations__question', 'translations__answer')
    readonly_fields = ('views', 'likes')