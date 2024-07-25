from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, CustomRole, CustomPermission


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
    email = forms.EmailField(required=True)
    facebook = forms.URLField(required=False)
    twitter = forms.URLField(required=False)
    profile_picture = forms.ImageField(widget=forms.FileInput, required=False)
    
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', 'facebook', 'twitter']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.user.email = self.cleaned_data['email']
        if commit:
            profile.user.save()
            profile.save()
        return profile


class CustomRoleForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=CustomPermission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = CustomRole
        fields = ['name', 'permissions']


class UserEditForm(forms.ModelForm):
    role = forms.ModelChoiceField(queryset=CustomRole.objects.all(), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'role']

    def clean_role(self):
        role = self.cleaned_data.get('role')
        if role and not CustomRole.objects.filter(id=role.id).exists():
            raise forms.ValidationError("Invalid role selected.")
        return role
    

