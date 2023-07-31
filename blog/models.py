from django.db import models
from django.urls import reverse

from users.models import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Cодержимое')
    image = models.ImageField(upload_to='blog/', verbose_name='Изображение', **NULLABLE)
    create_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    last_change_date = models.DateTimeField(verbose_name='Дата последнего изменения', auto_now=True)
    is_published = models.BooleanField(verbose_name='Признак публикации')
    count_views = models.IntegerField(verbose_name='Количество просмотров', default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:blog', args=[str(self.id)])

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-create_date']
