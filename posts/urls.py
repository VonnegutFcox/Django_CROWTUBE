# posts\urls.py
from django.urls import path
from rest_framework.authtoken import views
from . import views

app_name = "posts"

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),

    path("", views.index, name="index"),
    path("group/<slug:slug>/", views.group_posts, name="show_group"),
    path("new/", views.new_post, name="new_post"),

    path("follow/", views.follow_index, name="follow_index"),

    # Профайл пользователя
    path("<str:username>/", views.profile, name="profile"),

    # Просмотр записи
    path("<str:username>/<int:post_id>/", views.post_view, name="post"),
    path("<str:username>/<int:post_id>/edit/",
         views.post_edit, name="post_edit"),

    path("<str:username>/<int:post_id>/comment/",
         views.add_comment, name="add_comment"),

    path("<str:username>/follow/",
         views.profile_follow, name="profile_follow"),
    path("<str:username>/unfollow/",
         views.profile_unfollow, name="profile_unfollow"),
]
