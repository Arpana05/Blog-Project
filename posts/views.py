from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Like, Category   
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from .forms import PostForm, CommentForm, ChangeCategoryForm
from django.http import HttpResponse
from users.models import User
from django.views import View
from django.contrib import messages


# Create your views here.


def check_role_permissions(user, required_permissions=None):
    if user.is_superuser:
        return True
    if user.is_authenticated and user.profile.role:
        if required_permissions is None:
            return True  # If no specific permissions are required, allow access
        user_permissions = set(user.profile.role.permissions.values_list('name', flat=True))
        return set(required_permissions).issubset(user_permissions)
    return False

def check_role(user, required_roles=None):
    if user.is_superuser:
        return True  # Superusers can be considered to have all roles

    if user.is_authenticated and user.profile.role:
        if required_roles is None:
            return True  # If no specific roles are required, allow access
        return user.profile.role.name in required_roles

    return False

@login_required
def post_view(request, username=None):
    """this function works as a view function for blog posts
    
    Keyword arguments:
    username -- to show the users posts
    Return: returns django template
    """
    
    if username:
        user = get_object_or_404(User, username=username)
        posts = Post.objects.filter(is_active=True, author=user)
        profile = user.profile
    else:
        user = request.user
        posts = Post.objects.filter(is_active=True, author=request.user)
        profile = user.profile if user.is_authenticated else None
    
    context = {
        'profile': user.profile,
        'posts': posts,
    }
    return render(request, 'post_view.html', context)


@login_required
@user_passes_test(lambda u: check_role_permissions(u, ['Can create post']))
def post_create(request):
    """sumary_line
    
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)  
    else:
        form = PostForm()

    categories = Category.objects.all()
    
    context = {
        'form': form,
        'categories': categories,
    }
    return render(request, 'post_create.html', context)


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'edit_post.html', context)


@login_required
@user_passes_test(lambda u: check_role_permissions(u, ['Can change category']))
def change_category(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = ChangeCategoryForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category changed successfully.')
            return redirect('post_detail', pk=post.pk)
    else:
        form = ChangeCategoryForm(instance=post)

    context = {
        'post': post,
        'form': form,
    }

    return render(request, 'change_category.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(enabled=True)
    comment_form = CommentForm()
    categories = Category.objects.all()

    liked = False
    if request.user.is_authenticated:
        liked = post.likes.filter(user=request.user).exists()

    if request.user == post.author:
        can_edit = True
    else:
        can_edit = False

    if request.method == 'POST':
        form = ChangeCategoryForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category changed successfully.')
            return redirect('post_detail', pk=post.pk)
    else:
        form = ChangeCategoryForm(instance=post)  # Initial form instantiation

    context = {
        'post': post,
        'categories': categories,
        'comments': comments,
        'liked': liked,
        'comment_form': comment_form,
        'can_edit': can_edit,
        'change_category_form': form, 
    }
    return render(request, 'post_detail.html', context)


@login_required
@user_passes_test(lambda u: check_role_permissions(u, ['Can add comment']))
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    categories = Category.objects.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()

    liked = post.likes.filter(user=request.user).exists()

    context = {
        'post': post,
        'categories': categories,
        'comments': comments,
        'comment_form': comment_form,
        'liked': liked,
    }
    return render(request, 'post_detail.html', context)


@login_required
@user_passes_test(lambda u: check_role_permissions(u, ['Can delete comment']))
def delete_comment(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    
    if request.user == comment.user:
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')

    return redirect('post_detail', pk=post_pk)



@login_required
@user_passes_test(lambda u: check_role_permissions(u, ['Can add like']))
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    liked = post.likes.filter(user=request.user).exists()

    if liked:
        post.likes.filter(user=request.user).delete()
    else:
        Like.objects.create(post=post, user=request.user)

    return redirect('post_detail', pk=pk)


@login_required
@user_passes_test(lambda u: check_role_permissions(u, ['Can edit post']))
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            updated_post = form.save(commit=False)
            if 'post_image' in request.FILES:
                updated_post.post_image = request.FILES['post_image']
            updated_post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'post_edit.html', context)

