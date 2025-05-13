import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#d4a05b+0*t*c8*ak$i=6u7q^*v5_r5kx%18nm&@ma*%5a^lk1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1:8000','phoenix-rapid-factually.ngrok-free.app','localhost:8000','*']
CORS_ALLOWED_ORIGINS = ['https://phoenix-rapid-factually.ngrok-free.app']
CSRF_TRUSTED_ORIGINS = [
    'https://phoenix-rapid-factually.ngrok-free.app',
    'http://localhost:8000',  # Include localhost for local testing
    'http://127.0.0.1:8000',  # Include 127.0.0.1 for local testing
]
LOGOUT_REDIRECT_URL = 'home'  # Logoutdan so'ng yo'naltiriladigan URL nomi

# Application definition

INSTALLED_APPS = [
    'unfold',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',
    'users',
    'crispy_forms',
    'crispy_bootstrap5',
    'accounts'
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.joinpath('templates')],
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

WSGI_APPLICATION = 'config.wsgi.application'

import dj_database_url
# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.parse("postgresql://main_b3k9_user:9hP4ejNGZhLAkZVFj59RQEGmKzFFf754@dpg-d0hjsm3uibrs739qnfqg-a.ohio-postgres.render.com/main_b3k9")
}



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'uz'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication settings
LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

# Crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

AUTH_PASSWORD_VALIDATORS = []
AUTHENTICATION_BACKENDS = [
    'users.backends.EmailBackend',  # Add your custom backend
    'django.contrib.auth.backends.ModelBackend',  # Keep the default as a fallback
]
from unfold.settings import CONFIG_DEFAULTS
AUTH_USER_MODEL = 'accounts.CustomUser'

UNFOLD = {
    **CONFIG_DEFAULTS,
    "SITE_TITLE": "Adminpanel",
    "SITE_HEADER": "Admin Panel",
    "SHOW_HISTORY": True,  
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "Main",
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",
                        "link": "/admin/",
                    },
                    {
                        "title": "Categories",
                        "icon": "category",
                        "link": "/admin/shop/category/",
                    },
                    {
                        "title": "Products",
                        "icon": "store",
                        "link": "/admin/shop/product/",
                    },
                    {
                        "title": "Comments",
                        "icon": "comment",
                        "link": "/admin/shop/comment/",
                    },
                    {
                        "title": "Replies",
                        "icon": "reply",
                        "link": "/admin/shop/reply/",
                    },
                    {
                        "title": "Ratings",
                        "icon": "star",
                        "link": "/admin/shop/rating/",
                    },
                    {
                        "title": "Product Views",
                        "icon": "visibility",
                        "link": "/admin/shop/productview/",
                    },
                ],
            },
        ],
    },
    "TABS": [
        {
            "models": [
                "shop.category",
                "shop.product",
                "shop.comment",
                "shop.reply",
                "shop.rating",
                "shop.productview",
            ],
            "items": [
                {
                    "title": "Categories",
                    "link": "/admin/shop/category/",
                },
                {
                    "title": "Products",
                    "link": "/admin/shop/product/",
                },
                {
                    "title": "Comments",
                    "link": "/admin/shop/comment/",
                },
                {
                    "title": "Replies",
                    "link": "/admin/shop/reply/",
                },
                {
                    "title": "Ratings",
                    "link": "/admin/shop/rating/",
                },
                {
                    "title": "Product Views",
                    "link": "/admin/shop/productview/",
                },
            ],
        },
    ],
}

