
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addpost", views.addpost, name='addpost'),
    path("allposts", views.allposts, name='allposts'),
    path("profile/<str:username>", views.viewprofile, name='profile'),
    path("editpost/<int:postid>", views.editpost, name='editpost'),
    path("followaction/<int:userid>", views.followaction, name='followaction'),
    path("followingposts", views.followingposts, name='followingposts'),
    path("likeaction/<int:postid>", views.likeaction, name='likeaction'),
]
