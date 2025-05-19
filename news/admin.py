from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import News, Category

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('translations__name',)

@admin.register(News)
class NewsAdmin(TranslatableAdmin):
    list_display = ('title', 'category', 'created_at', 'views', 'likes')
    list_filter = ('category', 'created_at')
    search_fields = ('translations__title', 'translations__content')
    date_hierarchy = 'created_at'
    readonly_fields = ('views', 'likes')
    
    def get_prepopulated_fields(self, request, obj=None):
        # Disable slug prepopulation for translated fields
        return {}