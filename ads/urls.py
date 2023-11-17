from django.urls import path
from .views import *

urlpatterns = [
    path('submit_form/', submit_ads, name='submit_ads'),
    path('success/<str:message>', success, name='success'),
    path('', ads_homepage, name='ads_home_page'),
    path('watch/<str:pk>', add_view, name='watch_add'),
    path('add_media/<str:path>', add_media, name='add_media'),
    path('try_again/', tryagain, name='tryagain'),
    path('submit_adrequest/', submit_add_request, name="sub_add_req"),
    path('my_ads/', my_ads, name="my_ads"),
]
