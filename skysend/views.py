from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import redirect

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from skysend.forms import MailingSettingsForm, MailingClientForm, MailingMessageForm
from skysend.models import MailingSettings, MailingClient, MailingMessage

from datetime import datetime
from django.utils import timezone

from skysend.services import datetime_send_next, cron_send_mail, one_send_mail


class MailingSettingsListView(PermissionRequiredMixin, ListView):
    """Просмотр рассылок"""
    model = MailingSettings
    extra_context = {
        'title': 'Мои рассылки'
    }
    permission_required = ['skysend.view_mailingsettings']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.request.user.is_staff:
            context['object_list'] = MailingSettings.objects.all()
        else:
            context['object_list'] = MailingSettings.objects.filter(owner=self.request.user)
        return context


class MailingSettingsDetailView(PermissionRequiredMixin, DetailView):
    """Просмотр одной рассылки"""
    model = MailingSettings
    permission_required = ['skysend.view_mailingsettings']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = context['object']
        if self.request.user.is_staff or self.request.user == self.object.owner:
            context['mailing_client'] = MailingClient.objects.filter(pk=self.object.pk)
        else:
            raise PermissionDenied()
        return context


class MailingSettingsCreateView(PermissionRequiredMixin, CreateView):
    """Создание рассылки"""
    model = MailingSettings
    form_class = MailingSettingsForm
    extra_context = {
        'title': 'Добавить рассылку'
    }
    permission_required = ['skysend.add_mailingsettings']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        mailing_client_formset = inlineformset_factory(MailingSettings, MailingClient, form=MailingClientForm, extra=1,
                                                       can_delete=False)
        mailing_message_formset = inlineformset_factory(MailingSettings, MailingMessage, form=MailingMessageForm,
                                                        extra=1, can_delete=False)
        if self.request.POST:
            context['mailing_client'] = mailing_client_formset(self.request.POST)
            context['mailing_message'] = mailing_message_formset(self.request.POST)
        else:
            context['mailing_client'] = mailing_client_formset(queryset=MailingClient.objects.none())
            context['mailing_message'] = mailing_message_formset(queryset=MailingMessage.objects.none())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        mailing_client = context['mailing_client']
        mailing_message = context['mailing_message']
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.owner = self.request.user
            self.object.mailing_date_next = datetime_send_next(
                begin_date=form.cleaned_data['begin_date'],
                end_date=form.cleaned_data['end_date'],
                time=form.cleaned_data['sending_time'],
                frequence=form.cleaned_data['intervals']
            )
            self.object.status_mailing = 'created'
            self.object.save()
        if mailing_client.is_valid():
            mailing_client.instance = self.object
            mailing_client.save()
        if mailing_message.is_valid():
            mailing_message.instance = self.object
            mailing_message.save()
        begin_datetime = datetime.combine(form.cleaned_data['begin_date'], form.cleaned_data['sending_time'])
        end_datetime = datetime.combine(form.cleaned_data['end_date'], form.cleaned_data['sending_time'])
        if begin_datetime < datetime.now() < end_datetime and timezone.now() < self.object.mailing_date_next:
            self.object.status_mailing = 'running'
            one_send_mail(self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('skysend:my_list_detail_send', kwargs={'pk': self.object.pk})


class MailingSettingsUpdateView(PermissionRequiredMixin, UpdateView):
    """Обновление рассылки"""
    model = MailingSettings
    form_class = MailingSettingsForm
    permission_required = ['skysend.change_mailingsettings']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.request.user != self.object.owner and not self.request.user.is_superuser:
            raise PermissionDenied()
        context['title'] = context['object']
        mailing_client_formset = inlineformset_factory(MailingSettings, MailingClient, form=MailingClientForm, extra=1,
                                                       can_delete=True)
        mailing_message_formset = inlineformset_factory(MailingSettings, MailingMessage, form=MailingMessageForm,
                                                        extra=1, can_delete=True)
        if self.request.POST:
            context['mailing_client'] = mailing_client_formset(self.request.POST, instance=self.object,
                                                               prefix="mailing_client")
            context['mailing_message'] = mailing_message_formset(self.request.POST, instance=self.object,
                                                                 prefix="mailing_message")
        else:
            context['mailing_client'] = mailing_client_formset(instance=self.object, prefix="mailing_client")
            context['mailing_message'] = mailing_message_formset(instance=self.object, prefix="mailing_message")
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        mailing_client = context['mailing_client']
        mailing_message = context['mailing_message']
        self.object = form.save()
        self.object.mailing_date_next = datetime_send_next(
            begin_date=form.cleaned_data['begin_date'],
            end_date=form.cleaned_data['end_date'],
            time=form.cleaned_data['sending_time'],
            frequence=form.cleaned_data['intervals']
        )
        if self.object.mailing_date_next < timezone.now() and form.cleaned_data['is_active']:
            self.object.is_active = False
            self.object.status_mailing = 'completed'
        elif not self.object.is_active:
            self.object.status_mailing = 'completed'
        else:
            self.object.status_mailing = 'edited'
        self.object.save()
        if mailing_client.is_valid():
            mailing_client.instance = self.object
            mailing_client.save()
        if mailing_message.is_valid():
            mailing_message.instance = self.object
            mailing_message.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('skysend:my_list_detail_send', kwargs={'pk': self.object.pk})


class MailingSettingsDeleteView(PermissionRequiredMixin, DeleteView):
    """Удаление рассылки"""
    model = MailingSettings
    permission_required = ['skysend.delete_mailingsettings']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = context['object']
        return context

    def get_success_url(self):
        return reverse_lazy('skysend:my_list_send')


def change_is_active(request, *args, **kwargs):
    """Процедура включения/отключения рассылки модератором"""
    if not request.user.is_staff:
        raise PermissionDenied()
    mailing_settings = MailingSettings.objects.get(pk=kwargs['pk'])
    if mailing_settings.is_active:
        mailing_settings.is_active = False
        mailing_settings.status_mailing = 'completed'
    else:
        mailing_date_next = datetime_send_next(
            begin_date=mailing_settings.begin_date,
            end_date=mailing_settings.end_date,
            time=mailing_settings.sending_time,
            frequence=mailing_settings.intervals
        )
        if mailing_date_next > timezone.now():
            mailing_settings.is_active = True
            mailing_settings.status_mailing = 'running'
            mailing_settings.mailing_date_next = mailing_date_next
    mailing_settings.save()
    return redirect(reverse_lazy('skysend:my_list_detail_send', kwargs={'pk': kwargs['pk']}))
