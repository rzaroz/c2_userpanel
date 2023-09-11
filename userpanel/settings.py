from pathlib import Path
import os, json

DIRECTORY = os.path.dirname((os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(DIRECTORY)
with open(PROJECT_DIR + '/env_var.json', 'r') as file:
    ENV = json.loads(file.read())

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-7-3r5j(5c1c5k^t279=3d&jkb4i3v6f4w(6td1fdvu9_x-qp4a'

DEBUG = ENV['DEBUG']
ALLOWED_HOSTS = ENV['ALLOWED_HOSTS'].split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'userpanelapp',
    'charity',
    'zarinpal'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'userpanel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'userpanel.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': ENV["DATABASE_ENGINE"],
        'NAME': ENV['DB_NAME'],
        'USER': ENV['DB_USER'],
        'PASSWORD': ENV['DB_PASSWORD'],
        'HOST': ENV['DB_HOST'],
        'PORT': ENV['DB_PORT'],
    }

}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'


if ENV["REAL_SERVER"]:
    STATIC_ROOT = BASE_DIR / "static_cdn" / "static_root"
else:
    STATICFILES_DIRS = [
        BASE_DIR / "assets"
    ]


MEDIA_URL = "media/"

MEDIA_ROOT = BASE_DIR / "static_cdn" / "media_root"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
