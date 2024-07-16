from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import SignUpForm, ProfileForm
from posts.forms import PostForm
from .models import Profile
from posts.models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


def index(request):
    recent_posts = Post.objects.order_by('-date_published')[:3]  # Fetch recent posts, adjust as needed
    context = {
        'recent_posts': recent_posts,
    }
    return render(request, 'index.html', context)

def world(request):
    posts = Post.objects.filter(category__name='World')
    return render(request, 'category_posts.html', {'posts': posts, 'category': 'World'})

def technology(request):
    posts = Post.objects.filter(category__name='Technology')
    return render(request, 'category_posts.html', {'posts': posts, 'category': 'Technology'})

def design(request):
    posts = Post.objects.filter(category__name='Design')
    return render(request, 'category_posts.html', {'posts': posts, 'category': 'Design'})

def culture(request):
    posts = Post.objects.filter(category__name='Culture')
    return render(request, 'category_posts.html', {'posts': posts, 'category': 'Culture'})

def politics(request):
    posts = Post.objects.filter(category__name='Politics')
    return render(request, 'category_posts.html', {'posts': posts, 'category': 'Politics'})

def science(request):
    posts = Post.objects.filter(category__name='Science')
    return render(request, 'category_posts.html', {'posts': posts, 'category': 'Science'})

def health(request):
    posts = Post.objects.filter(category__name='Health')
    return render(request, 'category_posts.html', {'posts': posts, 'category': 'Health'})

def travel(request):
    posts = Post.objects.filter(category__name='Travel')
    return render(request, 'category_posts.html', {'posts': posts, 'category': 'Travel'})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')  # Redirect to profile page after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')  # Redirect to homepage after signup
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


def backend_login(request):
    return render(request, 'backend_templates/backend_login.html')

def admin_required(user):
    return user.is_superuser

@login_required
@user_passes_test(admin_required)
def backend_dashboard(request):
    return render(request, 'backend_templates/backend_dashboard.html', {'title': 'Backend Dashboard'})

@login_required
def profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
        posts = Post.objects.filter(author=request.user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
        posts = []
    
    context = {
        'profile': profile,
        'user': request.user,
        'posts': posts,  # Pass posts to the template context
    }
    return render(request, 'profile.html', context)


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'form': form,
    }
    return render(request, 'edit_profile.html', context)

def all_posts(request):
    posts = Post.objects.all().order_by('-date_published')
    
    paginator = Paginator(posts, 5)  # Show 5 posts per page

    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'all_posts.html', {'page_obj': page_obj})

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get_or_create(user=user)[0]  
    
    context = {
        'profile': profile,
    }
    return render(request, 'profile_view.html', context)

def search_view(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    users = User.objects.filter(username__icontains=query)
    
    context = {
        'posts': posts,
        'users': users,
        'query': query
    }
    return render(request, 'search_results.html', context)


@login_required
@staff_member_required
def backend_dashboard(request):
    return render(request, 'backend_dashboard.html')

@login_required
@staff_member_required
def manage_users(request):
    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})

@login_required
@staff_member_required
def manage_posts(request):
    posts = Post.objects.all()
    return render(request, 'manage_posts.html', {'posts': posts})

@login_required
@staff_member_required
def manage_comments(request):
    comments = Comment.objects.all()
    return render(request, 'manage_comments.html', {'comments': comments})

@login_required
@staff_member_required
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('manage_users')

@login_required
@staff_member_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('manage_posts')
    # return render(request, 'delete_post.html', {'post': post})

@login_required
@staff_member_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('manage_comments')
    return render(request, 'delete_comment.html', {'comment': comment})
