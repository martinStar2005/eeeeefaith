from django.urls import path
from . import views

app_name = 'about'

urlpatterns = [
    path('', views.about, name='index'),
    path('contact/', views.contact, name='contact'),
]