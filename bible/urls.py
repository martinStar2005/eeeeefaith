from django.urls import path
from . import views

app_name = 'bible'

urlpatterns = [
    path('', views.bible_home, name='home'),
    path('book/<int:pk>/', views.book_detail, name='book'),
    path('book/<int:book_id>/chapter/<int:chapter_num>/', views.chapter_detail, name='chapter'),
    path('book/<int:book_id>/chapter/<int:chapter_num>/verse/<int:verse_num>/', views.verse_detail, name='verse'),
    path('search/', views.bible_search, name='search'),
]