from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Post, Comment, Group, Story


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', 'cover_photo', 'location', 'website', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Cosa stai pensando?'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Scrivi un commento...'}),
        }


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'cover_image', 'is_private']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Descrivi il tuo gruppo...'}),
        }


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['image', 'video', 'text_content', 'background_color']
        widgets = {
            'text_content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Scrivi qualcosa...', 'maxlength': 200}),
            'background_color': forms.TextInput(attrs={'type': 'color'}),
        }
