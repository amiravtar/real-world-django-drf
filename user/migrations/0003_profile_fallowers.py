# Generated by Django 5.0.1 on 2024-03-29 14:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0002_profile_token"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="fallowers",
            field=models.ManyToManyField(
                related_name="followings", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]