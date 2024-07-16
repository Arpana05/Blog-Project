from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
    profile_picture = forms.ImageField(required=False, help_text='Upload a profile picture', widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'profile_picture')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile_picture = self.cleaned_data.get('profile_picture')
            if profile_picture:
                profile = Profile.objects.create(user=user, profile_picture=profile_picture)
                profile.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', 'facebook', 'twitter']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
            'profile_picture': forms.FileInput(attrs={'accept': 'image/*'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bio'].label = 'Biography'
        self.fields['profile_picture'].label = 'Profile Picture'
