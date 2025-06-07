from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("new_page/", views.new_page, name="new_page"),
    path("add/", views.add, name="add"),
    path("<str:title>/e", views.edit_page, name="edit_page"),
    path("edit/", views.edit, name="edit"),
    path("random/", views.random, name="random")
]
