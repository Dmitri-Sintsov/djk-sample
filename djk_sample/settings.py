import random
import hashlib
from django.utils import timezone
# from django.utils.version import get_version
# from distutils.version import LooseVersion

"""
Django settings for djk_sample project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'r2d9#(n2%*)&15vt-+5&o3rkqg(@%b5$&agqy_vqw(t4ax(_wh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

JS_ERRORS_ALERT = DEBUG
# Requires proper setup of Django email error logging.
JS_ERRORS_LOGGING = not DEBUG

# ALLOWED_HOSTS = []

# Application definition

DJK_APPS = [
    'djk_sample',
    'club_app',
    'event_app',
]

# Order of installed apps is important for Django Template loader to find 'djk_sample/templates/base.html'
# before original allauth 'base.html' is found, when allauth DTL templates are used instead of built-in
# 'django_jinja_knockout._allauth' Jinja2 templates, thus DJK_APPS are included before 'allauth'.
#
# For the same reason, djk_ui app is included before django_jinja_knockout, to make it possible to override
# any of django_jinja_knockout template / macro.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'sites' is required by allauth
    'django.contrib.sites',
    'django_jinja',
    'django_jinja.contrib._humanize',
    'djk_ui',
    'django_jinja_knockout',
    'django_jinja_knockout._allauth',
] + DJK_APPS + [
    'allauth',
    'allauth.account',
    # Required for socialaccount template tag library despite we do not use social login
    'allauth.socialaccount',
]

# For simple cases it is enough to include original middleware (commented out).
DJK_MIDDLEWARE = 'djk_sample.middleware.ContextMiddleware'
# DJK_MIDDLEWARE = 'django_jinja_knockout.middleware.ContextMiddleware'

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    DJK_MIDDLEWARE,
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django_log.sql'),
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

ROOT_URLCONF = 'djk_sample.urls'

TEMPLATES = [
    {
        "BACKEND": "django_jinja.backend.Jinja2",
        "APP_DIRS": True,
        "OPTIONS": {
            "match_extension": ".htm",
            "app_dirname": "jinja2",
            'context_processors': [
                'django.template.context_processors.i18n',
                # For simple cases it is enough to include original template context processor (commented out).
                'djk_sample.context_processors.template_context_processor'
                # 'django_jinja_knockout.context_processors.template_context_processor'
            ]
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Next line is required only if project uses Django templates (DTL).
                'djk_sample.context_processors.template_context_processor'
            ],
        },
    },
]

WSGI_APPLICATION = 'djk_sample.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'TEST': {
            # 'NAME': ':memory:',
            'NAME': os.path.join(BASE_DIR, 'test.sqlite3'),
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

# Use django_jinja_knockout app.js / middleware.py to detect timezone from browser.
USE_JS_TIMEZONE = True

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

VUE_INTERPOLATION = False

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Next setting is required so multiple Django instances running at the same host/IP with different ports
# do not interfere each other (apollo13).
hash_obj = hashlib.md5(BASE_DIR.encode('utf-8'))
SESSION_COOKIE_NAME = 'djk_sessionid_{}'.format(hash_obj.hexdigest())

# As this is the test application, registration with SMTP confirmation is not supported.
# Use:
""" python manage.py createsuperuser """
# or:
"""
python manage.py shell
from django.contrib.auth.models import User
user = User.objects.create_user('user', email='user@gmail.com', password='djk12345')
user.save()
exit()
"""

# For 'allauth'.
SITE_ID = 1
# Prevents infinite redirect when user has no permission to access current view.
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False
ALLAUTH_DJK_URLS = True

# Login / logout for allauth.
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = "/"
LOGOUT_URL = '/accounts/logout/'

# Pagination settings.
OBJECTS_PER_PAGE = 3 if DEBUG else 10

# unit testing settings
FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'fixtures'),
)

random.seed(timezone.now().timestamp())
