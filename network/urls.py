
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:user_id>/<str:username>", views.profile, name="profile"),
    path("follow/<int:user_to_follow_id>/<int:toFollow>", views.follow, name='follow'),
    path("following", views.following_posts, name='following_posts'),
    path("posts/<int:post_id>", views.posts, name="posts"),
    path("write_post", views.write_post, name='write'),
    path("create_post", views.create_post, name="create_post")
]
