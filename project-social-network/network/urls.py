
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="post"),
    path('edit/<int:post_id>/', views.edit, name='edit'),
    path('save/<int:post_id>', views.save, name='save'),
    path('like/<int:post_id>', views.like, name='like'),
    path('like_refresh/<int:post_id>/', views.like_refresh, name='like_refresh'),
    path("profile", views.profile, name="profile"),
    path('profile_refresh', views.profile_refresh, name='profile_refresh'),
    path('profile_following/<int:following_id>', views.profile_following, name='profile_following'),
    path("following", views.following, name='following')
    
]
