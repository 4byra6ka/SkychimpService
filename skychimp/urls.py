from django.urls import path

from skychimp.apps import SkychimpConfig
from skychimp.views import MainView, main_view

app_name = SkychimpConfig.name

urlpatterns = [
    path('', main_view, name='main'),
    # path('', MainView.as_view(), name='main'),

]