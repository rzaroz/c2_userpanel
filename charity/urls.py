from django.urls import path
from .views import charityhome

urlpatterns = [
    path('', charityhome, name='charity'),

]