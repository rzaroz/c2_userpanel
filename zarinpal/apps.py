from django.apps import AppConfig
import os

from django.conf import settings


class ZarinpalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'zarinpal'
    verbose_name = "تراکنش ها و پرداخت ها"
    path = os.path.join(settings.BASE_DIR, 'zarinpal')
