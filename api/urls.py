from django.urls import path
from .views import UserRegistration, UserLogin, UserView,ProfileView,FollowUser,ArticleCreatListView

app_name = "api"
urlpatterns = [
    path("users", UserRegistration.as_view(), name="user_registration"),
    path("users/login", UserLogin.as_view(), name="user_login"),
    path("user", UserView.as_view(), name="user_get"),

    path("profiles/<str:user>", ProfileView.as_view(), name="profile_view"),
    path("profiles/<str:user>/follow", FollowUser.as_view(), name="profile_follow"),

    path("articles", ArticleCreatListView.as_view(), name="profile_follow"),
]
