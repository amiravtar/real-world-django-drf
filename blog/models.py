from django.db import models
from django.utils.text import slugify
# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey("user.Profile", on_delete=models.CASCADE)
    description = models.TextField()
    body = models.TextField()
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    tags = models.ManyToManyField("Tag", related_name="articles")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    favoritesCount = models.IntegerField(default=0)
    comments = models.ManyToManyField("Comment", related_name="articles")

    def save(self, *args, **kwargs):
        # Generate slug from the title if not provided
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    body = models.TextField()
