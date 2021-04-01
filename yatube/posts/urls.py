# posts\urls.py
from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path("", views.index, name="index"),
    path("group/<slug:slug>/", views.group_posts, name="show_group"),
    path("new/", views.new_post, name="new_post"),
]
