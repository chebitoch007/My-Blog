import os
import environ
from pathlib import Path

# Initialize environment
env = environ.Env()

# Set BASE_DIR correctly
BASE_DIR = Path(__file__).resolve().parent.parent

# Read .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# Read SECRET_KEY from environment, or crash if missing (safety check)
SECRET_KEY = env("SECRET_KEY")

# Read DEBUG from environment, default to False for production
DEBUG = env.bool("DEBUG", default=False)

# Allow hosts specified in environment (Render provides the URL dynamically)
# We default to allowing all (*) to make deployment easier, but you can restrict this later.
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=['*'])

# Trust Render's proxy to handle HTTPS correctly
CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chebitoch',
    'django_ckeditor_5',
    'storages',
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

ROOT_URLCONF = 'MyBlog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Django will look in app/templates/
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

WSGI_APPLICATION = 'MyBlog.wsgi.application'


# Database
DATABASES = {
    'default': env.db(),  # This automatically parses the DATABASE_URL
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# AWS S3 SETTINGS
# We use env.str() to get keys. If they exist, we use S3.
if env("AWS_ACCESS_KEY_ID", default=None):
    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = "eu-north-1"
    AWS_S3_SIGNATURE_VERSION = "s3v4"
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",
    }

    # This makes sure files overwrite enabled so you don't get messy filenames
    AWS_S3_FILE_OVERWRITE = False

    # "public-read" makes sure your blog images are visible to visitors (Changed to None after error)
    AWS_DEFAULT_ACL = None # Allow S3 Bucket Policy to handle permissions

    # This configures Django to use S3 for storage
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "location": "media",  # Stores media in a 'media' folder on S3
            },
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "location": "static",  # Stores static files in a 'static' folder on S3
            },
        },
    }

    # Point CKEditor 5 to the default storage (which is now S3)
    CKEDITOR_5_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    # Override URLs to point to S3
    STATIC_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/static/"
    MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/"

else:
    # LOCAL DEVELOPMENT SETTINGS (Keep these as they were)
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
    # Use local file storage for CKEditor locally
    CKEDITOR_5_FILE_STORAGE = "django_ckeditor_5.storage.FileSystemStorage"

"""
#STATIC_URL = 'static/'
# ================== Static & Media Files ==================
STATICFILES_DIRS = [
    BASE_DIR / 'chebitoch/static',
    BASE_DIR / 'static',
]
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

"""
# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ADMIN_URL = env("ADMIN_URL", default="admin")


# ================== GLOBAL STATIC FILES CONFIG ==================
# This tells Django where to look for your CSS/JS files locally
STATICFILES_DIRS = [
    BASE_DIR / 'chebitoch/static',
    BASE_DIR / 'static',
]

# ================== CKEDITOR CONFIGURATION ==================
CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading", "|",
            "bold", "italic", "underline", "strikethrough", "|",
            "bulletedList", "numberedList", "|",
            "link", "blockQuote", "|",
            "imageUpload", "mediaEmbed", "|",
            "undo", "redo"
        ],
        "height": "300px",
        "width": "100%",
        "language": "en",
    }
}