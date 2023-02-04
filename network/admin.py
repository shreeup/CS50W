from django.contrib import admin

from .models import Profile,Post,User

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Post)