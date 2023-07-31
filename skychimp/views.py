import random

from django.core.cache import cache
from django.shortcuts import render
from django.views.generic import FormView

from blog.models import Blog
from config.settings import CACHE_ENABLED
from skysend.models import MailingSettings, MailingClient


def main_view(request):
    """Контроллер главной страницы"""
    context = {
        'title': 'Главная страница'
    }
    return render(request, 'skychimp/main.html', get_cached_main(context))


def get_cached_main(context):
    """Кеш статистики"""
    if CACHE_ENABLED:
        context['blogs'] = cache.get('blogs')
        context['mailing_settings_count'] = cache.get('mailing_settings_count')
        context['mailing_settings_count_run'] = cache.get('mailing_settings_count_run')
        context['mailing_client_unique_count'] = cache.get('mailing_client_unique_count')
        if context['blogs'] is None:
            count_blog = len(Blog.objects.filter(is_published=True))
            if count_blog > 0:
                blog_3_post = random.sample(list(Blog.objects.filter(is_published=True)),
                                            count_blog if count_blog < 3 else 3)
                context['blogs'] = blog_3_post
            cache.set('blogs', context['blogs'])
        if context['mailing_settings_count'] is None:
            context['mailing_settings_count'] = MailingSettings.objects.count()
            cache.set('mailing_settings_count', context['mailing_settings_count'])
        if context['mailing_settings_count_run'] is None:
            context['mailing_settings_count_run'] = MailingSettings.objects.filter(status_mailing='running').count()
            cache.set('mailing_settings_count_run', context['mailing_settings_count_run'])
        if context['mailing_client_unique_count'] is None:
            context['mailing_client_unique_count'] = MailingClient.objects.all().distinct('sending_email').count()
            cache.set('mailing_client_unique_count', context['mailing_client_unique_count'])
    else:
        count_blog = len(Blog.objects.filter(is_published=True))
        if count_blog > 0:
            blog_3_post = random.sample(list(Blog.objects.filter(is_published=True)),
                                        count_blog if count_blog < 3 else 3)
            context['blogs'] = blog_3_post
        context['mailing_settings_count'] = MailingSettings.objects.count()
        context['mailing_settings_count_run'] = MailingSettings.objects.filter(status_mailing='running').count()
        context['mailing_client_unique_count'] = MailingClient.objects.all().distinct('sending_email').count()
    return context
