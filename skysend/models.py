from datetime import datetime

from django.conf import settings
from django.db import models

from users.models import User, NULLABLE


class MailingClient(models.Model):

    sending_email = models.EmailField(verbose_name='контактный email')
    fio = models.CharField(max_length=100, verbose_name='фио')
    comment = models.TextField(verbose_name='комментарий')

    def __str__(self):
        return f'{self.pk}:{self.sending_email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class MailingMessage(models.Model):
    email_subject = models.CharField(verbose_name='тема письма')
    email_body = models.TextField(verbose_name='тело письма')

    def __str__(self):
        return f'{self.email_subject}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingSettings(models.Model):
    SENDING_FREQUENCY_CHOICES = (
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('monthly', 'Ежемесячно'),
    )
    STATUS_MAILING_CHOICES = (
        ('created', 'Создана'),
        ('running', 'Запущена'),
        ('completed', 'Завершена'),
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE)
    sending_time = models.TimeField(default=datetime.now(), verbose_name='время рассылки')
    intervals = models.CharField(choices=SENDING_FREQUENCY_CHOICES, verbose_name='периодичность')
    status_mailing = models.CharField(choices=STATUS_MAILING_CHOICES, verbose_name='статус рассылки')
    mailing_client = models.ManyToManyField(MailingClient)
    mailing_message = models.ForeignKey(MailingMessage, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.pk}:{self.owner}'

    class Meta:
        verbose_name = 'Настройка рассылка'
        verbose_name_plural = 'Настройки рассылки'


class MailingStatus(models.Model):
    mailing_settings = models.ForeignKey(MailingSettings, on_delete=models.CASCADE)
    data_time_status = models.DateTimeField(verbose_name='дата и время последней попытки')
    attempted_status = models.BooleanField(verbose_name='статус попытки')
    mail_server_response = models.TextField(verbose_name='ответ почтового сервера')

    def __str__(self):
        return f'{self.pk}:{self.data_time_status} Статус:{self.attempted_status}'

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
