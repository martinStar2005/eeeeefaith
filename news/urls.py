from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.news_list, name='list'),
    path('category/<int:pk>/', views.category_news, name='category'),
    path('detail/<slug:slug>/', views.news_detail, name='detail'),
]