from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields

class Book(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("Book Name"), max_length=100),
    )
    order = models.PositiveIntegerField(_("Order"), unique=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('bible:book', kwargs={'pk': self.pk})

class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapters')
    number = models.PositiveIntegerField(_("Chapter Number"))
    
    class Meta:
        ordering = ['book__order', 'number']
        unique_together = ('book', 'number')
    
    def __str__(self):
        return f"{self.book.name} {self.number}"
    
    def get_absolute_url(self):
        return reverse('bible:chapter', kwargs={'book_id': self.book.id, 'chapter_num': self.number})

class Verse(TranslatableModel):
    translations = TranslatedFields(
        text=models.TextField(_("Verse Text")),
    )
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='verses')
    number = models.PositiveIntegerField(_("Verse Number"))
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['chapter__book__order', 'chapter__number', 'number']
        unique_together = ('chapter', 'number')
    
    def __str__(self):
        return f"{self.chapter} : {self.number}"
    
    def get_absolute_url(self):
        return reverse('bible:verse', kwargs={
            'book_id': self.chapter.book.id,
            'chapter_num': self.chapter.number,
            'verse_num': self.number
        })
    
    def get_reference(self):
        return f"{self.chapter.book.name} {self.chapter.number}:{self.number}"
    
    def increment_view_count(self):
        self.views += 1
        self.save(update_fields=['views'])