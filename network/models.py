from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    followers=models.ManyToManyField(User,related_name="followed_by",symmetrical=False,blank=True)
    followees=models.ManyToManyField(User,related_name="influencers",symmetrical=False,blank=True)

class Post(models.Model):
    poster = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes=models.ManyToManyField(User,related_name="liked_by",symmetrical=False,blank=True)
