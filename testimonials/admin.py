from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Testimony

@admin.register(Testimony)
class TestimonyAdmin(TranslatableAdmin):
    list_display = ('title', 'author', 'created_at', 'is_approved', 'views', 'likes')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('translations__title', 'translations__content', 'author')
    readonly_fields = ('views', 'likes')
    date_hierarchy = 'created_at'
    actions = ['approve_testimonies', 'disapprove_testimonies']
    
    def approve_testimonies(self, request, queryset):
        queryset.update(is_approved=True)
    approve_testimonies.short_description = "Approve selected testimonies"
    
    def disapprove_testimonies(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_testimonies.short_description = "Disapprove selected testimonies"