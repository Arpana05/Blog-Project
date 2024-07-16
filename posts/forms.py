from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    post_image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}))

    class Meta:
        model = Post
        fields = ['title','category', 'content', 'post_image']

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     if commit:
    #         user.save()
    #         post_image = self.cleaned_data.get('post_image')
    #         if post_image:
    #             post = Post.objects.create(user=user, post_image=post_image)
    #             post.save()
    #     return user


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

