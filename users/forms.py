from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from users.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'username or email',
            }
        )
    )

    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs = {
                'placeholder': 'password'
            }
        )
    )

    def clean(self):
        if self.request.method == 'POST':
            self.username = self.request.POST.get('email')
            self.password = self.request.POST.get('password')


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'fio', 'comment')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class UserRecoveryPasswordForm(forms.Form):
    email_recovery = forms.EmailField(label='Почта')
