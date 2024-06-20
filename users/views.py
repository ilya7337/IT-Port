from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import ProjectFile, Project, Profile, User, Subscription
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm, ProjectForm, ProjectFilesForm
import os
from django.contrib.auth import authenticate, login


def home(request: HttpRequest):
    projects = Project.objects.filter(is_visible_repository=True).order_by('-id')[:3]
    return render(request, 'users/home.html', {"projects": projects})


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'
    error_messages = {
        'invalid_login': (
            "Please enter a co "
            "fields may be case-sensitive."
        ),
        'inactive': ("This account is inactiйцуve."),
    }

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/')

        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=password)

            login(request, user)

            return redirect(to='users-home')

        return render(request, self.template_name, {'form': form})



class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
           
            self.request.session.set_expiry(0)

            self.request.session.modified = True

    
        return super(CustomLoginView, self).form_valid(form)

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Ваш пароль учаешно изменен"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        print(user_form.is_valid())
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Данныеу успесшно изменены')
            return redirect(to='users-profile')
        else:
            messages.error(request, 'Пожалуйста, вводите данные корреектно')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def project(request):
    if request.method == 'POST': 
        project_form = ProjectForm(request.POST)
        files_form = ProjectFilesForm(request.POST, request.FILES)
        if project_form.is_valid() and files_form.is_valid():
            project = project_form.save(commit=False)
            project.user = request.user
            project.save()
            
            for file in request.FILES.getlist('file'):
                ProjectFile.objects.create(project=project, file=file)
            messages.success(request, 'Проект успесшно сохранен')
            return redirect(to='users-profile')
        else:
            messages.error(request, 'Пожалуйста, вводите данные корреектно')
            return redirect(to='upload-project')
    else:
        project_form = ProjectForm()
        files_form = ProjectFilesForm()
    
    return render(request, 'users/upload-project.html', {'project_form': project_form, 'files_form': files_form})

@login_required
def my_projects(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'users/show-my-projects.html', {'projects': projects})

@login_required
def edit_project(request, project_id):
    project = Project.objects.get(id=project_id)
    files = project.project_files.all()
    files = [(file, os.path.basename(file.file.name)) for file in files]
    if request.method == 'POST':
        form_project = ProjectForm(request.POST, instance=project)
        files_form = ProjectFilesForm(request.POST, request.FILES)
        if form_project.is_valid():
            form_project.save()
            for file in request.FILES.getlist('file'):
                project.project_files.create(file=file)
            messages.success(request, 'Проект успешно изменен')
            return redirect(to='my-projects')
        else:
            messages.error(request, 'Пожалуйста, вводите данные корреектно')
            return render(request, 'users/edit-project.html', {'form_project': form_project, 'form_files': ProjectFilesForm(), 'files': files})
    else:
        form_project = ProjectForm(instance=project)
        files_form = ProjectFilesForm()
    return render(request, 'users/edit-project.html', {'form_project': form_project, 'files': files, 'form_files': files_form})


def delete_file(request, file_id):
    file = ProjectFile.objects.get(id=file_id)
    file.file.delete()
    file.delete()
    return redirect(request.META.get('HTTP_REFERER'))

def search(request: HttpRequest):
    search_inf = request.POST['search']
    users_all = User.objects.all()
    users = []
    for user in users_all:
        profile = user.profile
        if search_inf in user.username or search_inf in profile.programming_languages or search_inf in profile.additional_tools\
        or search_inf in profile.hard_skills or  search_inf in profile.soft_skills or\
        search_inf in profile.experience or  search_inf in profile.hackathons or search_inf in profile.articles or\
        search_inf in profile.foreign_language or in_projects(search_inf, user):
            users.append(user)
    if not users:
        return render(request, 'users/search.html', {'message': "Извините, по вашему запросу ничего не найдено"})
    return render(request, 'users/search.html', {"search_inf": search_inf, 'users': users})

def in_projects(search_inf, user: User):
    projects = Project.objects.filter(user=user)
    for proj in projects:
        if search_inf in proj.project_name or search_inf in proj.description or search_inf in proj.programming_languages or search_inf in proj.additional_tools:
            return True
    return False

def see_profile(request: HttpRequest, username: str):
    is_subscribed = False
    user = User.objects.get(username=username)
    try:
        if Subscription.objects.filter(user=user, subscribed_user=request.user).exists():
            is_subscribed = True
    except Exception:
        pass
    return render(request, 'users/see_profile.html', {'user_inf': user, 'is_subscribed': is_subscribed})

def see_projects(request: HttpRequest, username: str):
    user = User.objects.get(username=username)
    projects = user.project_set.filter(is_visible_repository=1)
    return render(request, 'users/see_projects.html', {'projects': projects, 'username': username})

def see_project(request: HttpRequest, project_id: int):
    project = Project.objects.get(id=project_id)
    files = project.project_files.all()
    files = [(file, os.path.basename(file.file.name)) for file in files]
    return render(request, 'users/see_project.html', {'project': project, 'files': files})

def subscribe(request: HttpRequest , username: str):
    user = User.objects.get(username=username)
    user.profile.count_subscriptions += 1
    user.save()
    subscription = User.objects.get(username=request.user)
    subscription.profile.count_subscribers += 1
    subscription.save()
    s = Subscription.objects.create(user=user, subscribed_user=subscription)
    s.save()
    return redirect('see-profile', username=username)

def unsubscribe(request: HttpRequest , username: str):
    user = User.objects.get(username=username)
    user.profile.count_subscriptions -= 1
    user.save()
    subscription = User.objects.get(username=request.user)
    subscription.profile.count_subscribers -= 1
    subscription.save()
    s = Subscription.objects.filter(user=user, subscribed_user=request.user).delete()
    return redirect('see-profile', username=username)


