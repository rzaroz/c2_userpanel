from django.urls import path
from .views import userpanel, setting

urlpatterns = [
    path('', userpanel, name="userpanel"),
    path('Setting', setting, name="setting"),
]
