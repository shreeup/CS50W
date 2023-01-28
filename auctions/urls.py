from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:listing_id>", views.listing, name="listing"),
    #path("<int:listing_id>/bid", views.bid, name="bid"),
    path("add", views.add, name='add'),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.categories, name="categories"),
    path("addwatch/<int:listing_id>", views.addwatch, name='addwatch'),
    path("addbid/<int:listing_id>", views.addbid, name='addbid'),
    path("addcomment/<int:listing_id>", views.addcomment, name='addcomment'),
    path("deactivate/<int:listing_id>", views.deactivate, name='deactivate'),
    path("watchlist", views.watchlist, name='watchlist'),
]
