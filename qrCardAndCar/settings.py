from pathlib import Path
import os, dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
LINE_CHANNEL_ACCESS_TOKEN = 'xHnaVuyXvKzJ0yi02gSPpjVJBEnWfMCRrmUsWpUhh16VnDYqkgaXKg0HwC1Ul/m4MyWdZTSW66OZb9L6Hw0rHd/StJ7Olu1ShFs5R3U/GIxQ7zXdrcjMIYQUPxYJ1ws4G2VX++lOFHU6msuKdZOqPwdB04t89/1O/w1cDnyilFU='   #((需要改))

LINE_CHANNEL_SECRET = '7ab67c9f982fb7fd0011e63c702a71c2'   #((需要改))

# SECRET_KEY = "django-insecure-9k9(y_$jl+x$h3a4jox3-28d15fq93dxmr=6)929yiktxsfoa%"
SECRET_KEY = os.environ.get('SECRET_KEY', default='your secret key')    # for Render deploy

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = 'RENDER' not in os.environ    # for Render deploy

ALLOWED_HOSTS = []    # for Render deploy

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)    # for Render deploy


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'import_export',
    'hailAndChartered.apps.HailandcharteredConfig',
    'keyCardTest.apps.KeycardtestConfig'
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",    
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "qrCardAndCar.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "qrCardAndCar.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# for Render deploy
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://postgres:postgres@localhost:5432/mysite',
        conn_max_age=600
    )
}

# DATABASES = {
# 	"default": dj_database_url.config(default=("postgres://carservicedb_user:hMFpYZblPQVXCnkWU7lDzdD1gdSVz0nX@dpg-ck74ico8elhc7380ns4g-a.oregon-postgres.render.com/carservicedb"))}   #((需要改))

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'zh-Hant'
TIME_ZONE = 'Asia/Taipei'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/"    # for Render deploy
if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' # for Render deploy

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
IMPORT_EXPORT_USE_TRANSACTIONS = True