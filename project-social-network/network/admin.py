from django.contrib import admin
from .models import User, Post, Following, Likes

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Following)
admin.site.register(Likes)