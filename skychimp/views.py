import random

from django.shortcuts import render
from django.views.generic import FormView

from blog.models import Blog


def main_view(request):
    # products_list = Product.objects.all()
    blog_3_post = random.sample(list(Blog.objects.filter(is_published=True)), 3)
    context = {
        # 'object_list': products_list,
        'title': 'Главная страница',
        'blogs': blog_3_post
    }


    return render(request, 'skychimp/main.html', context)


# class MainView(FormView):
#     template_name = 'skychimp/main.html'


