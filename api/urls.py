from django.urls import path
from .views import UserRegistrationAPIView,UserLoginAPIView
app_name="api"
urlpatterns = [
    path('users', UserRegistrationAPIView.as_view(), name='user_registration'),
    path('users/login', UserLoginAPIView.as_view(), name='user_login'),
]