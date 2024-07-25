from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CustomPermission(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class CustomRole(models.Model):
    name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField(CustomPermission, related_name='roles', blank=True)
    users = models.ManyToManyField(User, related_name='custom_roles', blank=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    facebook = models.URLField(max_length=200, blank=True, null=True)
    twitter = models.URLField(max_length=200, blank=True, null=True)
    role = models.ForeignKey(CustomRole, on_delete=models.CASCADE, blank=True, null=True)
    status = models.BooleanField(default=True)
    email = models.EmailField(max_length=254, blank=True, null=True)

    def __str__(self):
        return self.user.username
