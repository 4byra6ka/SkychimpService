from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import CustomLoginView, RegisterView, ProfileView, RecoveryPasswordView, verification_user, \
    UserListView, change_is_active

app_name = UsersConfig.name

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('recovery_password/', RecoveryPasswordView.as_view(), name='recovery_password'),
    path('success_register/<str:register_uuid>/', verification_user, name='success_register'),
    path('list_user/', UserListView.as_view(), name='list_user'),
    path('list_user/<int:pk>/is_active/', change_is_active, name='change_is_active')
]
