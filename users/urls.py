from django.urls import path
from users import views
from .views import signup_view
from posts import views as post_views
# from posts.views import PostCreateView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='home'),
    path('world/', views.world, name='world'),
    path('technology/', views.technology, name='technology'),
    path('design/', views.design, name='design'),
    path('culture/', views.culture, name='culture'),
    path('politics/', views.politics, name='politics'),
    path('science/', views.science, name='science'),
    path('health/', views.health, name='health'),
    path('travel/', views.travel, name='travel'),
    path('signup/', signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('backend/dashboard/', views.backend_dashboard, name='backend_dashboard'),
    path('backend/manage/users/', views.manage_users, name='manage_users'),
    path('backend/manage/posts/', views.manage_posts, name='manage_posts'),
    path('backend/manage/comments/', views.manage_comments, name='manage_comments'),
    path('backend/manage/users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('backend/manage/posts/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('backend/manage/comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),

    path('profile/', views.profile, name='profile'),
    path('editprofile/', views.edit_profile, name='edit_profile'),

    path('all_posts/', views.all_posts, name='all_posts'),

    path('profile/<str:username>/', views.profile_view, name='profile_view'),

    path('posts/create/', post_views.post_create, name='post_create'),

    path('search/', views.search_view, name='search'),

    # ### Add a URL pattern for handling form submission
    # path('submit/', post_views.submit_post, name='submit_post'),   


]

