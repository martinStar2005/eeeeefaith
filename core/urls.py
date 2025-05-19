from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.email_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('language/', views.change_language, name='change_language'),
    path('like/<str:content_type>/<int:object_id>/', views.like_object, name='like_object'),
    path('comment/<str:content_type>/<int:object_id>/', views.add_comment, name='add_comment'),
]