from django.urls import path
from unicodedata import name

from .views import *

urlpatterns = [
    path('', user_panel, name="userpanel"),
    path('setting', setting, name="setting"),
    path('ajax_get_rate', ajax_get_rate, name="get_rate"),
    path('search/', search, name="search"),
    path('service/', service, name="service"),
    path('ajax_add_service', ajax_add_service, name="add_service"),
    path('factor/<str:factor_id>', factor, name="factor"),
    path('factors/', factors, name="factors")
]
