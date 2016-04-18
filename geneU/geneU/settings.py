"""
Django settings for geneU project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket
from django.test.utils import teardown_test_environment


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ymtcjj6&7-!#g-rrv^4c1m5t-utxtsls3dtp401+1q3zgmty86'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# AUTH_USER_MODEL = 'core.models.UserProfile'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd party apps
    'neomodel',
    'rest_framework',
    'oauth2_provider',
    'django_extensions',
    'corsheaders',
    'account',
    'pinax_theme_bootstrap',
    'bootstrapform',
    'celery',
    'rest_framework_swagger',
    # 'django-celery',
    # project apps
    'core',
    'geneTree',
    'geoencoding_node_structure',
    'date_node_structure'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware'
    # 'account.middleware.LocaleMiddleware',
    # 'account.middleware.TimezoneMiddleware',
)

ROOT_URLCONF = 'geneU.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

TEMPLATE_CONTEXT_PROCESSORS = [
    "account.context_processors.account",
    'django.core.context_processors.request',
    'pinax_theme_bootstrap.context_processors.theme'
]

WSGI_APPLICATION = 'geneU.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'core.permissions.IsActive',
    )
}

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
    }
}

AUTHENTICATION_BACKENDS = (
    # 'oauth2_provider.backends.OAuth2Backend',
    # Uncomment following if you want to access the admin
    'django.contrib.auth.backends.ModelBackend',
)

"""
# Name of nodes to start
# here we have a single node
CELERYD_NODES = "w1"
# or we could have three nodes:
# CELERYD_NODES = "w1 w2 w3"
# Where to chdir at start.
CELERYD_CHDIR = "."
# Extra arguments to celeryd
CELERYD_OPTS = "--time-limit=300 --concurrency=8"
# Name of the celery config module.
CELERY_CONFIG_MODULE = "celeryconfig"
# %n will be replaced with the nodename.
# CELERYD_LOG_FILE = "/var/log/celery/%n.log"
# CELERYD_PID_FILE = "/var/run/celery/%n.pid"

# Workers should run as an unprivileged user.
CELERYD_USER = "celery"
CELERYD_GROUP = "celery"
"""
SWAGGER_SETTINGS = {
    'exclude_namespaces': [],
    'api_version': '0.1',
    'api_path': '/',
    'enabled_methods': [
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    'api_key': '',
    'is_authenticated': False,
    'is_superuser': False,
    'unauthenticated_user': 'django.contrib.auth.models.AnonymousUser',
    'permission_denied_handler': None,
    'resource_access_handler': None,
    'base_path':'helloreverb.com/docs',
    'info': {
        'contact': 'apiteam@wordnik.com',
        'description': 'This is a sample server Petstore server. '
                       'You can find out more about Swagger at '
                       '<a href="http://swagger.wordnik.com">'
                       'http://swagger.wordnik.com</a> '
                       'or on irc.freenode.net, #swagger. '
                       'For this sample, you can use the api key '
                       '"special-key" to test '
                       'the authorization filters',
        'license': 'Apache 2.0',
        'licenseUrl': 'http://www.apache.org/licenses/LICENSE-2.0.html',
        'termsOfServiceUrl': 'http://helloreverb.com/terms/',
        'title': 'Swagger Sample App',
    },
    'doc_expansion': 'none',
}

CORS_ORIGIN_ALLOW_ALL = False


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False
EMAIL_HOST = 'localhost'
EMAIL_PORT = '25'
# EMAIL_HOST_USER = os.environ['GMAIL']
# EMAIL_HOST_PASSWORD = os.environ['GMAIL_PSW']
# DEFAULT_FROM_EMAIL = os.environ['GMAIL']
# DEFAULT_TO_EMAIL = os.environ['GMAIL']


ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True

try:
    HOSTNAME = socket.gethostname()
except:
    HOSTNAME = 'localhost'
