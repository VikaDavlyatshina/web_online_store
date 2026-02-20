from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy
from .views import UserCreateView, email_verifications, ProfileView, ProfileUpdateView, logout_view

from users.apps import UsersConfig

app_name = UsersConfig.name


urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("email-confirm/<str:token>/", email_verifications, name="email_confirm"),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
]
