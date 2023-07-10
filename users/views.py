import uuid

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, FormView, CreateView

from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserRecoveryPasswordForm
from users.models import User


class CustomLoginView(LoginView):
    model = User
    template_name = 'users/login.html'
    form_class = UserLoginForm
    # success_url = redirect('main.main')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            return redirect('skychimp:main')
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            try:
                user = User.objects.get(username=form.cleaned_data['email'])
            except:
                messages.error(self.request, 'Username does not exist!')
            if user is not None:
                login(self.request, user)
                message = f'Hello {user.username}! You have been logged in'
                return redirect('skychimp:main')
            else:
                message = 'Login failed!'
        return render(
            self.request, 'users/login.html', context={'form': form, 'message': message})


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

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
    user = User.objects.get(register_uuid=kwargs['register_uuid'])
    if user.register_uuid == kwargs['register_uuid']:
        user.is_active = True
        user.save()
        messages.add_message(request, messages.INFO, f'Учетная запись {user.email} активирована')
    return redirect(reverse('users:login'))


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class RecoveryPasswordView(FormView):
    model = User
    template_name = 'users/recovery_password.html'
    form_class = UserRecoveryPasswordForm

    def form_valid(self, form, *args, **kwargs):
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
        form.add_error('email_recovery', 'Такого почтового ящика нету')
        return super().form_invalid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO,
                             f'Пароль направлен на Email: {self.object.cleaned_data["email_recovery"]}')
        return reverse_lazy('users:login')