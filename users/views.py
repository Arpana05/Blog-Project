from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_protect
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import SignUpForm, ProfileForm, CustomRoleForm
from posts.forms import PostForm, ChangeCategoryForm
from .models import Profile, CustomRole, CustomPermission
from posts.models import Post, Comment, Category
from django.db import IntegrityError
from django.db.models import Q
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError



def index(request):
    recent_posts = Post.objects.order_by('-date_published')[:3] 
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

@csrf_protect
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            subject = 'Welcome to our Blog'
            message = render_to_string('email.html', {'user': user})
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            login(request, user)
            return redirect('profile')  
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.profile.status:
                    login(request, user)
                    if user.profile.role.name == 'admin':
                        return redirect('backend')
                    else:
                        return redirect('home')
                else:
                    messages.error(request, "Your account is disabled. Please contact the administrator.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def backend(request):
    title= 'Backend'
    return render(request, 'backend_base.html', {'title':title})

@login_required
def backend_profile(request):
    title = 'Backend Profile'
    try:
        profile = Profile.objects.get(user=request.user)
        posts = Post.objects.filter(author=request.user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
        posts = []
    
    context = {
        'title': title,
        'profile': profile,
        'user': request.user,
        'posts': posts,
    }
    return render(request, 'backend_profile.html', context)

@login_required
def dashboard(request):
    title = 'Dashboard'
    total_posts = Post.objects.count()
    total_comments = Comment.objects.count()
    total_users = User.objects.count()
    total_disabled_posts = Post.objects.filter(is_active=False).count()
    recent_posts = Post.objects.order_by('-date_published')[:10]
    recent_comments = Comment.objects.order_by('-created_at')[:10]
    context = {
        'title': title,
        'total_posts': total_posts,
        'total_comments': total_comments,
        'total_users': total_users,
        'total_disabled_posts': total_disabled_posts,
        'recent_posts': recent_posts,
        'recent_comments': recent_comments,
    }

    return render(request, 'dashboard.html', context)

@login_required
def users(request):
    title = 'Users'
    profiles = Profile.objects.select_related('user', 'role').all()
    return render(request, 'users.html', {'profiles': profiles, 'title': title})


@login_required
def add_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        role_id = request.POST['role']
        status = 'status' in request.POST
        password = request.POST['password']
        profile_picture = request.FILES.get('profile_picture', None)

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            
            role = CustomRole.objects.get(id=role_id)
            profile = Profile.objects.create(user=user, role=role, status=status)

            if profile_picture:
                profile.profile_picture = profile_picture
                profile.save()

            return redirect('users')

        except IntegrityError:
            error_message = 'Username already exists.'
            roles = CustomRole.objects.all()  
            return render(request, 'add_user.html', {'error_message': error_message, 'roles': roles})

    else:
        roles = CustomRole.objects.all()
        return render(request, 'add_user.html', {'roles': roles})



@require_POST
@login_required
@user_passes_test(lambda u: check_role_permissions(u, ['Can manage user']))
def disable_user(request, user_id):
    if request.method == 'POST':
        profile = get_object_or_404(Profile, user_id=user_id)
        profile.status = False
        profile.save()
    return redirect('users')

@require_POST
@login_required
@user_passes_test(lambda u: check_role_permissions(u, ['Can manage user']))
def enable_user(request, user_id):
    if request.method == 'POST':
        profile = get_object_or_404(Profile, user_id=user_id)
        profile.status = True
        profile.save()
    return redirect('users')

@login_required
@user_passes_test(lambda u: check_role_permissions(u, ['Can edit user']))
def edit_user(request, user_id):
    profile = Profile.objects.get(user_id=user_id)
    
    if request.method == 'POST':
        try:
            username = request.POST['username']
            email = request.POST['email']
            bio = request.POST['bio']
            role_id = request.POST['role']
            status = request.POST.get('status') == 'on'
            
            profile.user.username = username
            profile.user.email = email
            profile.bio = bio
            profile.role = CustomRole.objects.get(id=role_id)
            profile.status = status
            
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
            
            profile.user.save()
            profile.save()
            
            return redirect('users')
        
        except IntegrityError:
            return render(request, 'edit_user.html', {'profile': profile, 'roles': CustomRole.objects.all(), 'error_message': 'Username already exists.'})
        except ValidationError as e:
            return render(request, 'edit_user.html', {'profile': profile, 'roles': CustomRole.objects.all(), 'error_message': str(e)})

    roles = CustomRole.objects.all()
    
    return render(request, 'edit_user.html', {'profile': profile, 'roles': roles})



@login_required
@user_passes_test(lambda u: check_role_permissions(u, ['Can delete user']))
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('users')



@login_required
@user_passes_test(lambda u: check_role_permissions(u, ['Can manage post']))
def posts(request):
    title = 'Posts'
    posts = Post.objects.all()
    return render(request, 'posts.html', {'posts': posts, 'title': title})


def disable_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        post.is_active = False
        post.save()
        messages.success(request, "The post has been disabled successfully.")
    return redirect('posts')

def enable_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        post.is_active = True
        post.save()
        messages.success(request, "The post has been enabled successfully.")
    return redirect('posts')

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post added successfully.')
            return redirect('posts')
    else:
        form = PostForm()

    categories = Category.objects.all()
    
    return render(request, 'create_post.html', {'form': form, 'categories': categories})


@login_required
def edit_category(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = ChangeCategoryForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts') 
    else:
        form = ChangeCategoryForm(instance=post)

    categories = Category.objects.all()
    
    return render(request, 'edit_category.html', {'form': form, 'categories':categories, 'post': post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, 'Post deleted successfully.')
    return redirect('posts')


@login_required
@user_passes_test(lambda u: check_role_permissions(u, ['Can manage comments']))
def comments(request):
    title = 'Comments'
    comments = Comment.objects.all()
    return render(request, 'comments.html', {'comments': comments, 'title': title})

@login_required
@require_POST
@user_passes_test(lambda u: check_role_permissions(u, ['Can manage comments']))
def enable_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.enabled = True
    comment.save()
    return redirect('comments')

@login_required
@require_POST
@user_passes_test(lambda u: check_role_permissions(u, ['Can manage comments']))
def disable_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.enabled = False
    comment.save()
    return redirect('comments') 



@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    messages.success(request, 'Comment deleted successfully.')
    return redirect('comments')



def check_role_permissions(user, required_permissions=None):
    if user.is_superuser:
        return True
    if user.is_authenticated and user.profile.role:
        if required_permissions is None:
            return True 
        user_permissions = set(user.profile.role.permissions.values_list('name', flat=True))
        return set(required_permissions).issubset(user_permissions)
    return False


@login_required
def profile(request):
    title = 'Profile'
    try:
        profile = Profile.objects.get(user=request.user)
        posts = Post.objects.filter(author=request.user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
        posts = []
    
    context = {
        'title': title,
        'profile': profile,
        'user': request.user,
        'posts': posts,
    }
    return render(request, 'profile.html', context)


@login_required
@user_passes_test(lambda u: check_role_permissions(u, ['Can edit profile']))
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            print(form.errors) 
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
        'user': request.user,
    }
    return render(request, 'edit_profile.html', context)



def all_posts(request):
    posts = Post.objects.filter(is_active=True).order_by('-date_published')[:5]

    return render(request, 'all_posts.html', {'posts': posts})



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
@user_passes_test(lambda u: check_role_permissions(u, ['Can manage role']))
def manage_roles(request):
    roles = CustomRole.objects.all()
    profiles = Profile.objects.select_related('user', 'role').all()
    permissions = CustomPermission.objects.all()
    form = CustomRoleForm()
        
    if request.method == 'POST':
        form = CustomRoleForm(request.POST)
        if form.is_valid():
            role = form.save(commit=False)
            role.save()
            role.permissions.set(request.POST.getlist('permissions'))  
            messages.success(request, 'Role created successfully.')
            return redirect('manage_roles')


    profiles = Profile.objects.select_related('user', 'role').all()

    context = {
        'roles': roles,
        'profiles': profiles,
        'permissions': permissions,
        'form': form,
    }
    return render(request, 'manage_roles.html', context)

@login_required
@user_passes_test(lambda u: check_role_permissions(u, ['Can add role']))
def add_role(request):
    users = User.objects.all()

    if request.method == 'POST':
        role_form = CustomRoleForm(request.POST)
        if role_form.is_valid():
            role = role_form.save()

            users_assigned = request.POST.getlist('users')
            user_statuses = request.POST.getlist('user_status')
            for user_id, status in zip(users_assigned, user_statuses):
                user_profile = Profile.objects.get(user_id=user_id)
                user_profile.role = role
                user_profile.status = status
                user_profile.save()

            messages.success(request, 'Role added successfully.')
            return redirect('manage_roles')
    else:
        role_form = CustomRoleForm()

    context = {
        'role_form': role_form,
        'users': users,
    }
    return render(request, 'add_role.html', context)


@login_required
@user_passes_test(lambda u: check_role_permissions(u, ['Can edit role']))
def edit_role(request, role_id):
    role = get_object_or_404(CustomRole, pk=role_id)
    profiles = Profile.objects.filter(role=role)
    permissions = role.permissions.all()
    users = User.objects.exclude(profile__role=role)

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'delete':
            role.delete()
            return redirect('manage_roles')
        else:
            role_form = CustomRoleForm(request.POST, instance=role)
            if role_form.is_valid():
                role_form.save()

                user_id = request.POST.get('user')
                if user_id:
                    user_profile = Profile.objects.get(user_id=user_id)
                    user_profile.role = role
                    user_profile.save()

                role.permissions.set(request.POST.getlist('permissions'))
                return redirect('manage_roles')

    else:
        role_form = CustomRoleForm(instance=role, initial={'permissions': role.permissions.all()})

    context = {
        'role': role,
        'form': role_form,
        'profiles': profiles,
        'permissions': permissions,
        'users': users,
    }
    return render(request, 'edit_role.html', context)




@login_required
@user_passes_test(lambda u: check_role_permissions(u, ['Can view permission']))
def view_permissions(request, role_id):
    role = get_object_or_404(CustomRole, id=role_id)
    permissions = role.permissions.all()

    context = {
        'role': role,
        'permissions': permissions,
    }
    return render(request, 'view_permissions.html', context)




