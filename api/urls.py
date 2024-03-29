from django.urls import path
from .views import UserRegistration,UserLogin,UserView
app_name="api"
urlpatterns = [
    path('users', UserRegistration.as_view(), name='user_registration'),
    path('users/login', UserLogin.as_view(), name='user_login'),
    path('user', UserView.as_view(), name='user_login'),
]