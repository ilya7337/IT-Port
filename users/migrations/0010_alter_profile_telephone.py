# Generated by Django 4.1.2 on 2024-05-14 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_projectfile_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='telephone',
            field=models.CharField(blank=True, max_length=17, null=True),
        ),
    ]