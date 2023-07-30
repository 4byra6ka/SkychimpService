from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    register_uuid = models.CharField(max_length=50, **NULLABLE)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
