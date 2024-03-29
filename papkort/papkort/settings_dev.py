"""local runserver settings"""

import os

from .settings import BASE_DIR

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "nzcm$_84@4qd6e^#yinut58p%r0+qlveqjcg8@7rvq@-t)zxv1"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Static Files
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
        },
    },
    'root': {
        'handlers': ['console'],
    }
}