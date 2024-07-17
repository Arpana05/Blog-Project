from django.contrib import admin
from django.urls import path
from . import views
# from posts.views import PostCreateView


urlpatterns = [
    path('', views.post_view, name='post_view'),  
    path('<str:username>/', views.post_view, name='post_view_by_user'),
    path('create/', views.post_create, name='post_create'),
    path('<int:pk>/detail/', views.post_detail, name='post_detail'),
    path('<int:pk>/like/', views.like_post, name='like_post'),
    path('<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),

    
]