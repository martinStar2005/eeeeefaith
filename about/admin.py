from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import About

@admin.register(About)
class AboutAdmin(TranslatableAdmin):
    list_display = ('name', 'email', 'updated_at')
    
    def has_add_permission(self, request):
        # Only allow one instance of about
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)