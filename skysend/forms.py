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
        fields = ('sending_time', 'intervals')
        # widgets = {
        #     'sending_time': forms.TimeField(),
        #     'intervals': forms.ChoiceField(choices=SENDING_FREQUENCY_CHOICES),
            # attrs = {'class': 'form-control', 'placeholder': 'Field1'}
            # , attrs = {'class': 'form-control', 'placeholder': 'Field2'}
            # 'field3': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Field3'}),
            # 'field4': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Field4'}),
        # }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["title"].widget.attrs.update({"class": "form-control"})
    #     self.fields["content"].widget.attrs.update({"class": "form-control", 'style': "height: 150px"})
    #     self.fields["image"].widget.attrs.update({"class": "form-control"})
    #     self.fields["is_published"].widget.attrs.update({"class": "form-check-input"})


# class UpdateBlogForm(forms.ModelForm):
#     class Meta:
#         model = Blog
#         fields = ('title', 'content', 'image', 'is_published')
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["title"].widget.attrs.update({"class": "form-control"})
#         self.fields["content"].widget.attrs.update({"class": "form-control", 'style': "height: 150px"})
#         self.fields["is_published"].widget.attrs.update({"class": "form-check-input"})

