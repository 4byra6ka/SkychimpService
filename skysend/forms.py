from django import forms

from skysend.models import MailingSettings, MailingClient, MailingMessage


class MailingClientForm(forms.ModelForm):

    class Meta:
        model = MailingClient
        fields = ['sending_email', 'fio', 'comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["comment"].widget.attrs.update({"rows": 2})


class MailingMessageForm(forms.ModelForm):

    class Meta:
        model = MailingMessage
        fields = ['email_subject', 'email_body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email_body"].widget.attrs.update({"rows": 2})


class MailingSettingsForm(forms.ModelForm):

    class Meta:
        model = MailingSettings
        fields = ('sending_time', 'begin_date', 'end_date', 'intervals', 'is_active')
