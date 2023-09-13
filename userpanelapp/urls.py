from django.urls import path
from .views import *

urlpatterns = [
    path('', user_panel, name="userpanel"),
    path('setting', setting, name="setting"),
    path('get_rate', ajax_get_rate, name="get_rate"),
    path('search/', search, name="search")
]
