# Generated by Django 5.0.3 on 2024-03-30 19:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0002_article_author_alter_article_slug"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="article",
            name="comments",
        ),
        migrations.AddField(
            model_name="comment",
            name="article",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="blog.article",
            ),
            preserve_default=False,
        ),
    ]
