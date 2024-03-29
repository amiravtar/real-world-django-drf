from django.db import models
from django.conf import settings


def image_location(instase, filename) -> str:
    return f"user/{instase.id}/profile_{filename}"


# Create your models here.
class Profile(models.Model):
    bio = models.CharField(blank=True, max_length=100)
    image = models.ImageField(upload_to=image_location)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, null=True, blank=True)
