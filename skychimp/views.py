import random

from django.shortcuts import render
from django.views.generic import FormView

from blog.models import Blog
from skysend.models import MailingSettings, MailingClient


def main_view(request):
    context = {
        'title': 'Главная страница'
    }
    count_blog = len(Blog.objects.filter(is_published=True))
    if count_blog > 0:
        blog_3_post = random.sample(list(Blog.objects.filter(is_published=True)), count_blog if count_blog < 3 else 3)
        context['blogs'] = blog_3_post
    context['mailing_settings_count'] = MailingSettings.objects.count()
    context['mailing_settings_count_run'] = MailingSettings.objects.filter(status_mailing='running').count()
    context['mailing_client_unique_count'] = MailingClient.objects.all().distinct('sending_email').count()
    return render(request, 'skychimp/main.html', context)
