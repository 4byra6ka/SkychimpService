import random

from django.shortcuts import render
from django.views.generic import FormView

from blog.models import Blog


def main_view(request):
    context = {
        'title': 'Главная страница'
    }
    count_blog = len(Blog.objects.filter(is_published=True))
    if count_blog > 0:
        blog_3_post = random.sample(list(Blog.objects.filter(is_published=True)), count_blog if count_blog < 3 else 3)
        context['blogs'] = blog_3_post
    return render(request, 'skychimp/main.html', context)
