# Generated by Django 4.2.3 on 2023-07-10 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('content', models.TextField(verbose_name='Cодержимое')),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog/', verbose_name='Изображение')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('last_change_date', models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')),
                ('is_published', models.BooleanField(verbose_name='Признак публикации')),
                ('count_views', models.IntegerField(default=0, verbose_name='Количество просмотров')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
                'ordering': ['-create_date'],
            },
        ),
    ]