from django.contrib import admin

from skysend.models import MailingSettings, MailingClient, MailingMessage, MailingStatus

admin.site.register(MailingSettings)
admin.site.register(MailingClient)
admin.site.register(MailingMessage)
admin.site.register(MailingStatus)
