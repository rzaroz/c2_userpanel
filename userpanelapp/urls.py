from django.urls import path
from .views import user_panel, setting

urlpatterns = [
    path('', user_panel, name="userpanel"),
    path('Setting', setting, name="setting"),
]
