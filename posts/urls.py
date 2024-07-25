from django.contrib import admin
from django.urls import path
from . import views
# from posts.views import PostCreateView


urlpatterns = [
    path('', views.post_view, name='post_view'),  
    path('<str:username>/', views.post_view, name='post_view_by_user'),
    path('create/', views.post_create, name='post_create'),
    path('<int:pk>/detail/', views.post_detail, name='post_detail'),
    path('<int:pk>/add_comment/', views.add_comment, name='add_comment'),
    path('posts/<int:post_pk>/delete_comment/<int:comment_pk>/', views.delete_comment, name='delete_comment'),
    path('<int:pk>/like/', views.like_post, name='like_post'),
    path('<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('posts/<int:pk>/change_category/', views.change_category, name='change_category'),

    
]