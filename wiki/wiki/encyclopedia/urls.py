from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("add/", views.add, name="add"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random/", views.random_entry, name="random_entry")
]
