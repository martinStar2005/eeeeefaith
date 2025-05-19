from django.contrib import admin
from .models import SiteSettings, Comment

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'tagline', 'updated_at')
    
    def has_add_permission(self, request):
        # Only allow one instance of site settings
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'content_type', 'object_id', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at', 'content_type')
    search_fields = ('name', 'email', 'content')
    actions = ['approve_comments', 'disapprove_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approve selected comments"
    
    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_comments.short_description = "Disapprove selected comments"