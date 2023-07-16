from django.shortcuts import render
from django.views.generic import ListView, DetailView

from skysend.models import MailingSettings


class MailingSettingsListView(ListView):
    model = MailingSettings
    extra_context = {
        'title': 'Мои рассылки'
    }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # all_product = Product.objects.all()
        # context['all_product_list'] = all_product
        # context['object_sends_list'] = MailingSettings.objects.filter(is_a) # Product.active_version()
        # mailing_settings = MailingSettings.objects.get_queryset()
        # context['object_sends_list'] = mailing_settings.
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        # queryset.
        # if self.request.user.is_staff or self.request.user.groups.filter(name='moderators').exists():
        #     return queryset
        # else:
        #     return queryset
        #     queryset = queryset.filter(is_published=True)
        return queryset


class MailingSettingsDetailView(DetailView):
    model = MailingSettings
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = context['object']
        # context['is_edit'] = True
        # if self.object.owner != self.request.user and not self.request.user.is_superuser and not self.request.user.is_staff:
        #     context['is_edit'] = False
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        # queryset.
        # if self.request.user.is_staff or self.request.user.groups.filter(name='moderators').exists():
        #     return queryset
        # else:
        #     return queryset
        #     queryset = queryset.filter(is_published=True)
        return queryset