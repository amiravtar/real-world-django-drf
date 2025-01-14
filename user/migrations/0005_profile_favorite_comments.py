# Generated by Django 5.0.3 on 2024-03-29 17:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0001_initial"),
        ("user", "0004_rename_fallowers_profile_followers"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="favorite_comments",
            field=models.ManyToManyField(
                related_name="favorited_by", to="blog.article"
            ),
        ),
    ]
