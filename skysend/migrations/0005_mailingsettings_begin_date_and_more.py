# Generated by Django 4.2.3 on 2023-07-29 12:25

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('skysend', '0004_mailingsettings_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailingsettings',
            name='begin_date',
            field=models.DateField(default=datetime.datetime(2023, 7, 29, 15, 21, 47, 639152), verbose_name='Начала рассылки'),
        ),
        migrations.AddField(
            model_name='mailingsettings',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата создания'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mailingsettings',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2023, 7, 29, 12, 25, 0, 531311, tzinfo=datetime.timezone.utc), verbose_name='Окончание рассылки'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mailingsettings',
            name='sending_time',
            field=models.TimeField(default=datetime.datetime(2023, 7, 29, 15, 21, 47, 639118), verbose_name='время рассылки'),
        ),
    ]