"""
Django settings for colegio project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

from django.core.urlresolvers import reverse_lazy
from os.path import dirname, join, exists, os, sys
from decouple import config, Csv


# Build paths inside the project like this: join(BASE_DIR, "directory")
BASE_ROOT = dirname(dirname(dirname(dirname(__file__))))

BASE_DIR = dirname(dirname(dirname(__file__)))

EXTERNAL_LIBS_PATH = os.path.join(BASE_DIR,"externals","libs")

EXTERNAL_APPS_PATH = os.path.join(BASE_DIR, "externals", "apps")

sys.path = ["", EXTERNAL_LIBS_PATH, EXTERNAL_APPS_PATH] + sys.path

STATICFILES_DIRS = [join(BASE_DIR, 'static')]

MEDIA_ROOT = join(BASE_DIR, 'media')

MEDIA_URL = "/media/"

# Use Django templates using the new Django 1.8 TEMPLATES settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(BASE_DIR, 'templates'),
            # insert more TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Use 12factor inspired environment variables or from a file
import environ
env = environ.Env()

# Ideally move env file should be outside the git repo
# i.e. BASE_DIR.parent.parent
try:
    env_file = join(dirname(__file__), 'local.env')
except NameError:
    import sys
    env_file = join(dirname(sys.argv[0]), 'local.env')


if exists(env_file):
    environ.Env.read_env(str(env_file))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Raises ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')

# Application definition

INSTALLED_APPS = (
    'dal',
    'dal_select2',
    'django.contrib.auth',
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'authtools',
    'crispy_forms',
    'easy_thumbnails',

    'utils',
    'accounts',
    'cash',
    'enrollment',
    'income',
    'profiles',
    'register',
    'payments',
    'discounts',
    'import_export',
    'AE_academico',
    'django_filters',

)
IMPORT_EXPORT_USE_TRANSACTIONS = True

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'utils.middleware.ThreadLocalMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
)

"""
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://54.207.24.126/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {'max_connections': 100},
            #"CONNECTION_POOL_CLASS": "myproj.mypool.MyOwnPool",
            #"PARSER_CLASS": "redis.connection.HiredisParser",
            #"PASSWORD": "1234",
        },
        #"KEY_PREFIX": "colegio"
    }
}




SESSION_ENGINE = "django.contrib.sessions.backends.cache"

SESSION_CACHE_ALIAS = "default"

CACHE_TTL = 60 * 15
"""

ROOT_URLCONF = 'colegio.urls'

WSGI_APPLICATION = 'colegio.wsgi.application'

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {

    'default': env.db(),
    'TEST': env.db(),
}


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'es-PE'

TIME_ZONE = 'America/Lima'

USE_I18N = False

USE_L10N = False

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/' #% get_git_changeset(BASE_DIR)

# Crispy Form Theme - Bootstrap 3
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# For Bootstrap 3, change error alert to 'danger'
from django.contrib import messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

# Authentication Settings
AUTH_USER_MODEL = 'authtools.User'
#LOGIN_REDIRECT_URL = reverse_lazy("profiles:show_self")
LOGIN_REDIRECT_URL = reverse_lazy("accounts:tocolegio_self")
LOGIN_URL = reverse_lazy("accounts:login")

THUMBNAIL_EXTENSION = 'png'     # Or any extn for your thumbnails

REDIRECT_PERMISOS = '/about/'

