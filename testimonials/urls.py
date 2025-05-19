from django.urls import path
from . import views

app_name = 'testimonials'

urlpatterns = [
    path('', views.testimony_list, name='list'),
    path('detail/<slug:slug>/', views.testimony_detail, name='detail'),
    path('submit/', views.submit_testimony, name='submit'),
    path('featured/', views.featured_testimonies, name='featured'),
]