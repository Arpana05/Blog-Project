from django import forms
from .models import Post, Comment, Category

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'content', 'post_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'post_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     if commit:
    #         user.save()
    #         post_image = self.cleaned_data.get('post_image')
    #         if post_image:
    #             post = Post.objects.create(user=user, post_image=post_image)
    #             post.save()
    #     return user

class ChangeCategoryForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Write your comment here...'})
        }

class LikeForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = []

