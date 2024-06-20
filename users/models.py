from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.png', upload_to='profile_images')
    bio = models.TextField(max_length=500)
    telephone = models.CharField(blank=True, null=True, max_length=17)
    count_subscriptions = models.IntegerField(default=0)
    count_subscribers = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    programming_languages = models.CharField(blank=True, max_length=200)
    additional_tools = models.CharField(blank=True, max_length=200)
    hard_skills = models.CharField(blank=True, max_length=200)
    soft_skills = models.CharField(blank=True, max_length=200)
    experience = models.CharField(blank=True, max_length=200)
    hackathons = models.CharField(blank=True, max_length=200)
    articles = models.CharField(blank=True, max_length=200)
    foreign_language = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


class Project(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    project_name = models.CharField(blank=True, max_length=50)
    description = models.CharField(blank=True, max_length=300)
    programming_languages = models.CharField(blank=True, max_length=50)
    additional_tools = models.CharField(blank=True, max_length=200)
    is_visible_repository = models.BooleanField(default=False)


def project_files_path(instance: "ProjectFile", filename: str):
    # count_proj = len(os.listdir("media/projects/project_{instance.project.pk}"))
    return "projects/project_{pk}/files/{filename}".format(pk=instance.project.pk, filename=filename)  


class ProjectFile(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_files')
    file = models.FileField(upload_to=project_files_path)

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    subscribed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribed_user')

    class Meta:
        unique_together = ('user', 'subscribed_user')


