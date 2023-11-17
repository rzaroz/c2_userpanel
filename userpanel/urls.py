# from django.contrib import admin
import os, json

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

DIRECTORY = os.path.dirname((os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(DIRECTORY)
with open(PROJECT_DIR + '/env_var.json', 'r') as file:
    ENV = json.loads(file.read())

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('userpanelapp.urls')),
    path("charity/", include("charity.urls")),
    path("pay/", include("zarinpal.urls")),
    path("ads/", include("ads.urls")),
]

if ENV["REAL_SERVER"]:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
