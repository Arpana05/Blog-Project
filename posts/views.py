from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Like, Category   
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm, LikeForm
from django.http import HttpResponse
from users.models import User

# Create your views here.



@login_required
def post_view(request, username=None):
    """this function works as a view function for blog posts
    
    Keyword arguments:
    username -- to show the users posts
    Return: returns django template
    """
    
    if username:
        user = get_object_or_404(User, username=username)
        posts = Post.objects.filter(author=user)
    else:
        posts = Post.objects.filter(author=request.user)
    
    context = {
        'posts': posts,
    }
    return render(request, 'post_view.html', context)


@login_required
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
            return redirect('post_detail', pk=post.pk)  # Redirect to post_view with the pk of the newly created post
    else:
        form = PostForm()

    categories = Category.objects.all()
    
    context = {
        'form': form,
        'categories': categories,
    }
    return render(request, 'post_create.html', context)


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    comment_form = CommentForm()
    categories = Category.objects.all()

    liked = post.likes.filter(user=request.user).exists()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)

    context = {
        'post': post,
        'categories': categories,
        'comments': comments,
        'comment_form': comment_form,
        'liked': liked,
    }
    return render(request, 'post_detail.html', context)


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    liked = post.likes.filter(user=request.user).exists()

    if liked:
        post.likes.filter(user=request.user).delete()
    else:
        Like.objects.create(post=post, user=request.user)

    return redirect('post_detail', pk=pk)


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    categories = Category.objects.all()
    
    context = {
        'form': form,
        'categories': categories,
    }
    return render(request, 'post_edit.html', context)


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.user == post.author:
        post.delete()
        return redirect('all_posts')  
    else:
        return redirect('post_detail', pk=pk)

