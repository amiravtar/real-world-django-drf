from django.urls import path
from .views import (
    UserRegistration,
    UserLogin,
    UserView,
    ProfileView,
    FollowUser,
    ArticleCreatListView,
    ArticleFeedListView,
    ArticleDetailView,
    ArticleFavoriteView
)

app_name = "api"
urlpatterns = [
    #users
    path("users", UserRegistration.as_view(), name="user_registration"),
    path("users/login", UserLogin.as_view(), name="user_login"),
    path("user", UserView.as_view(), name="user_get"),
    #profiles
    path("profiles/<str:user>", ProfileView.as_view(), name="profile_view"),
    path("profiles/<str:user>/follow", FollowUser.as_view(), name="profile_follow"),
    #articles
    path("articles", ArticleCreatListView.as_view(), name="article_create_list"),
    path("articles/feed", ArticleFeedListView.as_view(), name="article_feed"),
    path("articles/<slug:slug>/favorite", ArticleFavoriteView.as_view(), name="article_favorite"),
    path("articles/<slug:slug>", ArticleDetailView.as_view(), name="article_detail"),
]
