# Generated by Django 2.1.12 on 2020-01-15 02:09

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('afordeal88scrumy', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ScrumyGoal',
            new_name='ScrumyGoals',
        ),
    ]