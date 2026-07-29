import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")
print("DB_HOST =", os.environ.get("DB_HOST"))

# ── Security — env se lo ──
SECRET_KEY    = os.environ.get('SECRET_KEY', '0kjdklji#jflkdjkjjdksjlkmvj94890uerejksdj')
DEBUG         = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost,k8s-library-libraryi-2e189b1376-1174569033.ap-south-1.elb.amazonaws.com').split(',')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'customer',
    'books',
    'author',
    'users',
    'tailwind',
    'theme',
]

TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = ['127.0.0.1']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Library_Management.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'Library_Management.wsgi.application'

# ── Database — env se lo (local default rakha) ──
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     os.environ.get('DB_NAME',     'library_db'),
        'USER':     os.environ.get('DB_USER',     'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'root@123'),
        'HOST':     os.environ.get('DB_HOST',     'localhost'),
        'PORT':     os.environ.get('DB_PORT',     '3306'),
        'OPTIONS':  {'charset': 'utf8mb4'},
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'Asia/Kolkata'
USE_I18N      = True
USE_TZ        = True

STATIC_URL       = '/static/'
STATIC_ROOT      = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL  = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Razorpay — env se lo ──
RAZORPAY_KEY_ID     = os.environ.get('RAZORPAY_KEY_ID',     '')
RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', '')