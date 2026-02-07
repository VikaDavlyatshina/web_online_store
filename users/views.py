import secrets

from django.contrib.auth import logout
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from config.settings import EMAIL_HOST_USER

from users.forms import UserRegisterForm
from users.models import User

# Create your views here.


class UserCreateView(CreateView):
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет! Для подтверждения почты перейдите пожалуйста по ссылке: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=True,
        )

        return super().form_valid(form)


def email_verifications(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


def logout_view(request):
    logout(request)
    return redirect("home")
