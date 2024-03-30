from django.contrib import admin
from blog.models import Article,Tag,Comment
# Register your models here.

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Tag)