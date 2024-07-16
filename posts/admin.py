from django.contrib import admin
from posts.models import Post, Like, Comment, Category

# Register your models here.

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Category)
