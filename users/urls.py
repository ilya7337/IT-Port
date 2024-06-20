from django.urls import path
from .views import home, profile, RegisterView, project, my_projects, edit_project,\
        search, see_profile, see_projects, delete_file, see_project, subscribe, unsubscribe

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('upload-project', project, name='upload-project'),
    path('my-projects/', my_projects, name='my-projects'),
    path('edit-project/<int:project_id>/', edit_project, name='edit-project'),
    path('search-result/', search, name='search'),
    path('delete-file/<int:file_id>', delete_file, name='delete-file'),
    path('profile/<str:username>', see_profile, name='see-profile'),
    path('projects/<str:username>', see_projects, name='see-projects'),
    path('project/<int:project_id>', see_project, name='see-project'),
    path('subscribe/<str:username>', subscribe, name='subscribe'),
    path('unsubscribe/<str:username>', unsubscribe, name='unsubscribe'),
]
