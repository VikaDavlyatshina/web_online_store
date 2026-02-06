from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy
from .views import UserCreateView, email_verifications

from users.apps import UsersConfig

app_name = UsersConfig.name


urlpatterns = [
    path("login/", LoginView.as_view(template_name='users/login.html'), name="login"),
    path("logout/", LogoutView.as_view(next_page=reverse_lazy('catalog:product_list')), name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
    path('email-confirm/<str:token>/', email_verifications, name='email_confirm'),

]
