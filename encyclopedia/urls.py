from django.urls import path,re_path

from . import views

from . import util

basepagespath_re = "(?=("+'|'.join(util.list_entries())+r"))"


urlpatterns = [
    path("", views.index, name="index"),
    #path(basepagespath_re, views.detailview, name="detailview")
    #re_path(basepagespath_re, views.detailview, name='detailview'),
    path("search", views.search, name='search'),
    path("random", views.random, name="random"),
    path("add", views.add, name='add'),
    path("<str:vname>", views.detailview, name="detailview"),
    
    
    path("update/<str:name>", views.update, name='update')
    
]

#handler404 = "encyclopedia.views.handler404"