from django.urls import path

from skysend.apps import SkySendConfig
from skysend.views import MailingSettingsListView, MailingSettingsDetailView

app_name = SkySendConfig.name

urlpatterns = [
    path("mylist/", MailingSettingsListView.as_view(), name="my_list_send"),
    path("mylist/<int:pk>/", MailingSettingsDetailView.as_view(), name="my_list_detail_send"),
]
