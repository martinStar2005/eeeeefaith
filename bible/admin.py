from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Book, Chapter, Verse

@admin.register(Book)
class BookAdmin(TranslatableAdmin):
    list_display = ('name', 'order')
    search_fields = ('translations__name',)
    ordering = ('order',)

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('book', 'number')
    search_fields = ('number',)
    list_filter = ('book',)

@admin.register(Verse)
class VerseAdmin(TranslatableAdmin):
    list_display = ('reference', 'chapter', 'number', 'views', 'likes')
    list_filter = ('chapter__book',)
    search_fields = ('translations__text', 'reference')
    readonly_fields = ('views', 'likes')
    
    def reference(self, obj):
        return f"{obj.chapter.book.name} {obj.chapter.number}:{obj.number}"
    reference.short_description = "Reference"