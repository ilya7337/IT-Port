from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import re

from .models import Profile, Project, ProjectFile


class RegisterForm(UserCreationForm):
    # fields we want to include and customize in our form
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя',
                                                             'class': 'form-control',
                                                             }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Пароль',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Пароль',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class UpdateUserForm(forms.ModelForm):

    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email']

def validate_telephone(value):
    if value and not re.match(r'^\+?1?\d{9,15}$', value):
        raise Exception('Please enter a valid telephone number (e.g. +1-555-555-5555).')
    
class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'file-btn'}), required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': '', 'rows': 5}), required=False)
    telephone = forms.CharField(required=False, validators=[validate_telephone])
    programming_languages = forms.CharField(widget=forms.Textarea, required=False)
    additional_tools = forms.CharField(widget=forms.Textarea, required=False)
    hard_skills = forms.CharField(widget=forms.Textarea, required=False)
    soft_skills = forms.CharField(widget=forms.Textarea, required=False)
    experience = forms.CharField(widget=forms.Textarea, required=False)
    hackathons = forms.CharField(widget=forms.Textarea, required=False)
    articles = forms.CharField(widget=forms.Textarea, required=False)
    foreign_language = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Profile
        fields = ['avatar', 'programming_languages', 'telephone', 'additional_tools',
        'hard_skills', 'soft_skills', 'experience', 'hackathons', 'articles', 'foreign_language']




class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = 'project_name', 'description', 'programming_languages', 'additional_tools', 'is_visible_repository'

    description = forms.CharField(widget=forms.Textarea, required=False)
    programming_languages = forms.CharField(widget=forms.Textarea, required=False)
    additional_tools = forms.CharField(widget=forms.Textarea, required=False)
    project_name = forms.CharField(widget=forms.Textarea, required=False)
    is_visible_repository = forms.BooleanField(widget=forms.CheckboxInput, required=False)

class ProjectFilesForm(forms.ModelForm):
    class Meta:
        model = ProjectFile
        fields = ('file',)
    
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))



