from django.urls import path
from users import views
from .views import signup_view
from posts import views as post_views


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
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('backend/', views.backend, name="backend"),
    path('backend_profile/', views.backend_profile, name='backend_profile'),
    path('backend/dashboard/', views.dashboard, name='dashboard'),
    path('backend/users/', views.users, name='users'),
    path('backend/manage/users/add/', views.add_user, name='add_user'),
    path('disable_user/<int:user_id>/', views.disable_user, name='disable_user'),
    path('enable_user/<int:user_id>/', views.enable_user, name='enable_user'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('users/delete/<int:user_id>', views.delete_user, name='delete_user'),
    path('backend/posts/', views.posts, name='posts'),
    path('backend/posts/create/', views.create_post, name='create_post'),
    path('edit_category/<int:post_id>/', views.edit_category, name='edit_category'),
    path('disable_post/<int:post_id>/', views.disable_post, name='disable_post'),
    path('enable_post/<int:post_id>/', views.enable_post, name='enable_post'),
    path('posts/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('backend/comments/', views.comments, name='comments'),
    path('enable_comment/<int:comment_id>/', views.enable_comment, name='enable_comment'),
    path('disable_comment/<int:comment_id>/', views.disable_comment, name='disable_comment'),
    path('comments/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),

    path('profile/', views.profile, name='profile'),
    path('editprofile/', views.edit_profile, name='edit_profile'),

    path('all_posts/', views.all_posts, name='all_posts'),

    path('profile/<str:username>/', views.profile_view, name='profile_view'),

    path('posts/create/', post_views.post_create, name='post_create'),

    path('search/', views.search_view, name='search'),


    path('manage-roles/', views.manage_roles, name='manage_roles'),
    path('add_role/', views.add_role, name='add_role'),
    path('edit_role/<int:role_id>/', views.edit_role, name='edit_role'),

    path('view_permissions/<int:role_id>/', views.view_permissions, name='view_permissions'),


]

