import uuid

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.contrib.auth.views import LoginView
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, FormView, CreateView, ListView

from blog.models import Blog
from skysend.models import MailingSettings
from users.forms import UserRegisterForm, UserProfileForm, UserRecoveryPasswordForm, UserLoginForm
from users.models import User


class CustomLoginView(FormView):
    """Контроллер входа пользователя"""
    model = User
    template_name = 'users/login.html'
    form_class = UserLoginForm
    extra_context = {
        'title': 'Войти'
    }

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            return redirect('skychimp:main')
        if form.is_valid():
            try:
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = User.objects.get(email=email)
                if user.check_password(password):
                    login(self.request, user)
                    perm_mailings_settings = Permission.objects.filter(
                        content_type=ContentType.objects.get_for_model(MailingSettings))
                    if user.is_staff:
                        perm_blog = Permission.objects.filter(content_type=ContentType.objects.get_for_model(Blog))
                        perm_user = Permission.objects.filter(content_type=ContentType.objects.get_for_model(User))
                        for perm in perm_blog:
                            user.user_permissions.add(perm)
                        user.user_permissions.add(perm_mailings_settings.get(codename='view_mailingsettings'))
                        user.user_permissions.add(perm_user.get(codename='change_user'))
                    else:
                        for perm in perm_mailings_settings:
                            user.user_permissions.add(perm)
                    return redirect('skychimp:main')
                else:
                    messages.add_message(self.request, messages.WARNING, 'Неправельный пользователь или пароль')
            except:
                messages.add_message(self.request, messages.WARNING, 'Неправельный пользователь или пароль')
            else:
                message = 'Login failed!'
        return render(
            self.request, 'users/login.html', context={'form': form})


class RegisterView(CreateView):
    """Контроллер регистрации пользователя"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    extra_context = {
        'title': 'Регистрация'
    }

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.is_active = False
            self.object.register_uuid = uuid.uuid4().hex
            self.object.save()
            current_site = get_current_site(self.request)
            send_mail(
                subject='Верификация пользователя',
                message=f'Верификация пользователя пройдите по ссылке http://{current_site}{reverse_lazy("users:success_register", kwargs={"register_uuid": self.object.register_uuid})}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.object.email]
            )
            return super().form_valid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO,
                             f'Пользователь создан. Пройдите верификацию. Данные направлена на Email: {self.object.email}')
        return reverse_lazy('users:login')


def verification_user(request, *args, **kwargs):
    """Функция верификации пользователя"""
    user = User.objects.get(register_uuid=kwargs['register_uuid'])
    if user.register_uuid == kwargs['register_uuid']:
        user.is_active = True
        user.save()
        messages.add_message(request, messages.INFO, f'Учетная запись {user.email} активирована')
    return redirect(reverse('users:login'))


class ProfileView(UpdateView):
    """Обновление профиля"""
    model = User
    form_class = UserProfileForm
    extra_context = {
        'title': 'Данные профиля'
    }

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Данные профиля изменены')
        return reverse_lazy('users:profile')


class RecoveryPasswordView(FormView):
    """Контроллер восстановления пароля"""
    model = User
    template_name = 'users/recovery_password.html'
    form_class = UserRecoveryPasswordForm
    extra_context = {
        'title': 'Восстановление пароля'
    }

    def form_valid(self, form, *args, **kwargs):
        try:
            recovery_user = User.objects.get(email=form.cleaned_data['email_recovery'])
            self.object = form
            if recovery_user and form.is_valid():
                password = User.objects.make_random_password()
                recovery_user.set_password(password)
                recovery_user.save()
                send_mail(
                    subject='Новый пароль',
                    message=f'Ваш новый пароль: {password}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[recovery_user.email]
                )
                return super().form_valid(form, *args, **kwargs)
        except:
            messages.add_message(self.request, messages.WARNING, 'Неправельная почта')
        return super().form_invalid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO,
                             f'Пароль направлен на Email: {self.object.cleaned_data["email_recovery"]}')
        return reverse_lazy('users:login')


class UserListView(PermissionRequiredMixin, ListView):
    """Список пользователей для staff """
    model = User
    extra_context = {
        'title': 'Список пользователей'
    }
    permission_required = ['users.change_user']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['object_list'] = User.objects.filter(is_staff=False)
        return context


def change_is_active(request, *args, **kwargs):
    """Процедура включения/отключения пользователя модератором"""
    if not request.user.is_staff:
        raise PermissionDenied()
    user = User.objects.get(pk=kwargs['pk'])
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect(reverse_lazy('users:list_user'))
