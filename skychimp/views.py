from django.shortcuts import render
from django.views.generic import FormView


def main_view(request):
    # products_list = Product.objects.all()
    context = {
        # 'object_list': products_list,
        'title': 'Главная страница'
    }
    return render(request, 'skychimp/main.html', context)


class MainView(FormView):
    template_name = 'skychimp/main.html'


