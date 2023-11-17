from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.send_request, name='request'),
    path('verify/', views.verify, name='pay_verify'),
    path('add_balance', views.add_balance, name="add_balance"),
]
