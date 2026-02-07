import secrets
from django.contrib import messages

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView

from config.settings import EMAIL_HOST_USER

from users.forms import UserRegisterForm, UserProfileForm
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

        messages.success(self.request, "Регистрация успешна! Проверьте почту для подтверждения.")
        return super().form_valid(form)


def email_verifications(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.token = None  # Удаляем токен после подтверждения
    user.save()
    messages.success(request, "Почта подтверждена! Теперь вы можете войти.")
    return redirect(reverse("users:login"))


def logout_view(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect("home")


class ProfileView(LoginRequiredMixin, View):
    """Страница просмотра профиля"""
    def get(self, request):
        context = {
            'user': request.user,
        }
        return render(request, 'users/profile.html', context)

# Редактирование профиля
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Страница редактирования профиля"""
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile')

    # Ключевой момент: переопределяем get_object
    def get_object(self, queryset=None):
        # Возвращаем текущего пользователя, без использования pk из URL
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлен!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)