from django.forms import inlineformset_factory

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from skysend.forms import MailingSettingsForm, MailingClientForm, MailingMessageForm
from skysend.models import MailingSettings, MailingClient, MailingMessage


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
        context['mailing_client'] = MailingClient.objects.filter(pk=self.object.pk)
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


class MailingSettingsCreateView(CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    extra_context = {
        'title': 'Добавить рассылку'
    }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        mailing_client_formset = inlineformset_factory(MailingSettings, MailingClient, form=MailingClientForm, extra=1, can_delete=False)
        mailing_message_formset = inlineformset_factory(MailingSettings, MailingMessage, form=MailingMessageForm, extra=1, can_delete=False)
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
            self.object.status_mailing = 'created'
            self.object.save()
        if mailing_client.is_valid():
            for mailing_client_form in mailing_client:
                mailing_client = mailing_client_form.save(commit=False)
                mailing_client.mailing_settings = self.object
                mailing_client.save()
        if mailing_message.is_valid():
            for mailing_message_form in mailing_message:
                mailing_message = mailing_message_form.save(commit=False)
                mailing_message.mailing_settings = self.object
                mailing_message.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('skysend:my_list_detail_send', kwargs={'pk': self.object.pk})


class MailingSettingsUpdateView(UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = context['object']
        mailing_client_formset = inlineformset_factory(MailingSettings, MailingClient, form=MailingClientForm, extra=1, can_delete=True)
        mailing_message_formset = inlineformset_factory(MailingSettings, MailingMessage, form=MailingMessageForm, extra=1, can_delete=True)
        if self.request.POST:
            context['mailing_client'] = mailing_client_formset(self.request.POST, instance=self.object, prefix="mailing_client")
            context['mailing_message'] = mailing_message_formset(self.request.POST, instance=self.object, prefix="mailing_message")
        else:
            context['mailing_client'] = mailing_client_formset(instance=self.object, prefix="mailing_client")
            context['mailing_message'] = mailing_message_formset(instance=self.object, prefix="mailing_message")
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        mailing_client = context['mailing_client']
        mailing_message = context['mailing_message']
        self.object = form.save()
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


class MailingSettingsDeleteView(DeleteView):
    model = MailingSettings

    def get_success_url(self):
        return reverse_lazy('skysend:my_list_send')
