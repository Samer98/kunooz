"""
Django settings for kunooz project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from datetime import timedelta
import sys
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _ # Here
load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-z8j&u#%q%apgrr5$7mvzf4muv)g1)vsl6t-i9mm(+h2_tiov8i'
# SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
# DEBUG = os.getenv("DEBUG", "False") == "True"
# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")
verify_sid = os.getenv("verify_sid")
verified_number = os.getenv("verified_number")



# DOMAIN = 'seashell-app-plyq6.ondigitalocean.app'
DOMAIN = os.getenv("DOMAIN", "127.0.0.1:8000")
DEBUG = os.getenv("DEBUG", True)
DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", True)
DEBUG = str(DEBUG).lower() == "true"
DEVELOPMENT_MODE = str(DEVELOPMENT_MODE).lower() == "true"

# ALLOWED_HOSTS = ['seashell-app-plyq6.ondigitalocean.app']

# Application definition
# SITE_ID = 2
# LOGIN_REDIRECT_URL = '/home'
# LOGOUT_REDIRECT_URL = '/home'


INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'members',
    'constructions',
    'additional_modification',
    'progress_step',
    'approval',
    'report',
    'note',
    'notifcations',
    'pricing_tender',


    'multiselectfield',
    'corsheaders',
]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "social_django.middleware.SocialAuthExceptionMiddleware",
]

ROOT_URLCONF = 'kunooz.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

WSGI_APPLICATION = 'kunooz.wsgi.application'
ASGI_APPLICATION = "kunooz.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# print("the connections here",dj_database_url.parse(os.environ.get("DATABASE_URL")))
# DEVELOPMENT_MODE = True

if DEVELOPMENT_MODE is True:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'kunooz',
            'HOST': 'localhost',
            'USER': 'root1',
            'PASSWORD': 'rootroot12345'
        }
    }
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
    if os.getenv("DATABASE_URL", None) is None:
        raise Exception("DATABASE_URL environment variable not defined")
    DATABASES = {
        "default": dj_database_url.parse(os.environ.get("DATABASE_URL")),}
    DATABASES['default']['OPTIONS'] = {
        'sslmode': 'require',  # Set the SSL mode to 'require' or the appropriate value
        'sslrootcert': '/path/to/ca_certificate.pem',
        'sslcert': '/path/to/client_certificate.pem',
        'sslkey': '/path/to/client_key.pem',
    }
    del DATABASES['default']['OPTIONS']['sslmode']
    del DATABASES['default']['OPTIONS']['sslrootcert']
    del DATABASES['default']['OPTIONS']['sslcert']
    del DATABASES['default']['OPTIONS']['sslkey']
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'members.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE':10,

    'DEFAULT_RENDERER_CLASSES':(
              'kunooz.globalView.CustomRenderer',
    #           'rest_framework.renderers.JSONRenderer',
    #           'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'EXCEPTION_HANDLER': 'kunooz.globalView.custom_exception_handler'
}
DJOSER = {
    'SERIALIZERS': {
        "user_create": 'members.serializers.UserCreateSerializer',
        "current_user": 'members.serializers.UserSerializer',
    },
    # 'EMAIL': {
    #         'password_reset': 'djoser.email.PasswordResetEmail',
    #         'password_changed_confirmation': 'djoser.email.PasswordChangedConfirmationEmail',
    #     }
    # ,

    'LOGIN_FIELD': 'phone_number',
    # 'USER_CREATE_PASSWORD_RETYPE':True,
    # 'ACTIVATION_URL': 'members/activate/{uid}/{token}',
    # 'SEND_ACTIVATION_EMAIL': True,
    # 'SEND_CONFIRMATION_EMAIL': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    "PASSWORD_RESET_CONFIRM_URL": "members/reset_password/{uid}/{token}",  # the reset link     'SET_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': True,
    'USERNAME_RESET_SHOW_EMAIL_NOT_FOUND': True,
    'TOKEN_MODEL': True,
    "SOCIAL_AUTH_TOKEN_STRATEGY": "djoser.social.token.jwt.TokenStrategy",
    "SOCIAL_AUTH_ALLOWED_REDIRECT_URIS": ["http://127.0.0.1:8000"],
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=36500),  # Set to a very large value
    'REFRESH_TOKEN_LIFETIME': timedelta(days=36500), # Set to a very large value
}

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = (
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

USE_L10N = True
# Available Languages
LANGUAGES = [
    ('ar', _('Arabic')),
    ('en', _('English')),
]
# Locales available path

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale/')
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_URL = "/static/"
STATICFILES_DIRS =[
    os.path.join(BASE_DIR,'static')
]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'consultantapp872@gmail.com'
# EMAIL_HOST_PASSWORD = 'pwpokeiynoeynrco'
# EMAIL_USE_TLS = True


# CORS_ALLOWED_ORIGINS = os.getenv(list("CORS_ALLOWED_ORIGINS", default=[]))
CORS_ALLOW_CREDENTIALS = True

# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv("GOOGLE_CLIENT_ID")
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv("GOOGLE_SECRET")
# SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
#     "https://www.googleapis.com/auth/userinfo.email",
#     "https://www.googleapis.com/auth/userinfo.profile",
#     "openid",
# ]
# AUTHENTICATION_BACKENDS = (
# 'social_core.backends.google.GoogleOAuth2',
# 'django.contrib.auth.backends.ModelBackend',
#
# )