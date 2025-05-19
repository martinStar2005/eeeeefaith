from django.urls import path
from . import views

app_name = 'faq'

urlpatterns = [
    path('', views.faq_home, name='home'),
    path('category/<int:pk>/', views.category_questions, name='category'),
    path('question/<int:pk>/', views.question_detail, name='detail'),
    path('search/', views.faq_search, name='search'),
]