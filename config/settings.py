from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-*t4=0b+(s18gs_^3c*05%5i$ru222y7r#h-8!!sky(ot2=y@$j')

# ⚠️ Production safe
DEBUG = False

# ✅ IMPORTANT FIX (Render needs full domain)
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "interviewhub-qnxf.onrender.com",
]

# ✅ CSRF fix (must include https + domain)
CSRF_TRUSTED_ORIGINS = [
    "https://interviewhub-qnxf.onrender.com",
]




INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'portal',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # must be here
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ---------------- DATABASE ----------------
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'interviewhub',
#        'USER': 'root',
#        'PASSWORD': 'Vasu@123',
#        'HOST': 'localhost',
#        'PORT': '3306',
#    }
#}
# ---------------- DATABASE ----------------
import dj_database_url

if os.environ.get('RENDER'):
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'interviewhub',
            'USER': 'root',
            'PASSWORD': 'Vasu@123',
            'HOST': 'localhost',
            'PORT': '3306',
            
        }
    }

# ---------------- PASSWORD VALIDATION ----------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]

# ---------------- INTERNATIONALIZATION ----------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# ---------------- STATIC FILES (IMPORTANT FIX) ----------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / "static"]

# WhiteNoise production fix
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ---------------- LOGIN ----------------
LOGIN_URL = '/login/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Render ke liye session fix

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')