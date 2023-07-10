from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from users.models import User


class UserLoginForm(forms.Form):
    email = forms.EmailField(label='', widget=forms.TextInput(
        attrs={'placeholder': "Почта", 'class': 'form-control', 'type': 'email'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder': "Пароль", 'class': 'form-control', 'type': 'password'}))


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"type": "email_recovery"})
        for field_name, field in self.fields.items():
            if field_name == 'email' or field_name == 'password1' or field_name == 'password2':
                field.widget.attrs['class'] = 'form-control'


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'fio', 'comment')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'email' or field_name == 'fio' or field_name == 'comment':
                field.widget.attrs['class'] = 'form-control'
            if field_name == 'comment':
                field.widget.attrs['style'] = "height: 100px"
            if field_name == 'email':
                field.widget.attrs['type'] = "email_recovery"


class UserRecoveryPasswordForm(forms.Form):
    email_recovery = forms.CharField(label='Почта')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'email_recovery':
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = "name@example.com"
                field.widget.attrs['type'] = "email_recovery"
