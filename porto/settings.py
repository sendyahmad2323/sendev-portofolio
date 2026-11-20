
"""Konfigurasi Django SenDev untuk lokal dan Vercel."""

import os
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured


# =====================================================
# 1. DIREKTORI PROYEK DAN ENVIRONMENT
# =====================================================
BASE_DIR = Path(__file__).resolve().parent.parent

IS_VERCEL = (
    os.environ.get("VERCEL") == "1"
    or bool(os.environ.get("VERCEL_ENV"))
)

DEBUG = os.environ.get(
    "DJANGO_DEBUG", "0" if IS_VERCEL else "1"
) == "1"

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "").strip()

if IS_VERCEL and not SECRET_KEY:
    raise ImproperlyConfigured(
        "DJANGO_SECRET_KEY wajib diatur di Environment Variables Vercel."
    )

if not SECRET_KEY:
    SECRET_KEY = "local-development-only-change-this-key"


# =====================================================
# 2. DOMAIN SENDEV
# =====================================================
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "sendev-portofolio.vercel.app",
    "sendev-tech.vercel.app",
]

ALLOWED_HOSTS += [
    host.strip()
    for host in os.environ.get(
        "DJANGO_ALLOWED_HOSTS", ""
    ).split(",")
    if host.strip()
]

ALLOWED_HOSTS = list(dict.fromkeys(ALLOWED_HOSTS))

CSRF_TRUSTED_ORIGINS = [
    "https://sendev-portofolio.vercel.app",
    "https://sendev-tech.vercel.app",
]

CSRF_TRUSTED_ORIGINS += [
    origin.strip()
    for origin in os.environ.get(
        "DJANGO_CSRF_TRUSTED_ORIGINS", ""
    ).split(",")
    if origin.strip()
]

CSRF_TRUSTED_ORIGINS = list(dict.fromkeys(CSRF_TRUSTED_ORIGINS))


# =====================================================
# 3. APLIKASI DJANGO
# =====================================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Cloudinary
    "cloudinary_storage",
    "cloudinary",

    # SenDev
    "portofolio.apps.PortofolioConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "porto.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "porto.wsgi.application"


# =====================================================
# 4. DATABASE: NEON (VERCEL) / SQLITE (LOKAL)
# =====================================================
DATABASE_URL = os.environ.get(
    "DATABASE_URL", ""
).strip()

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=0,
            conn_health_checks=True,
        )
    }

elif IS_VERCEL:
    raise ImproperlyConfigured(
        "DATABASE_URL wajib diatur di Vercel (PostgreSQL Neon)."
    )

else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# =====================================================
# 5. VALIDASI PASSWORD
# =====================================================
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# =====================================================
# 6. BAHASA DAN WAKTU
# =====================================================
LANGUAGE_CODE = "id"
TIME_ZONE = "Asia/Makassar"
USE_I18N = True
USE_TZ = True


# =====================================================
# 7. STATIC FILES DAN MEDIA STORAGE
# =====================================================

# Static files: CSS, JavaScript, ikon
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Media lokal hanya untuk development
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Kredensial Cloudinary dari environment
CLOUDINARY_URL = os.environ.get(
    "CLOUDINARY_URL", ""
).strip()

# Vercel wajib menggunakan Cloudinary
if IS_VERCEL and not CLOUDINARY_URL:
    raise ImproperlyConfigured(
        "CLOUDINARY_URL belum tersedia di Vercel. "
        "Tambahkan pada Settings > Environment Variables "
        "(Production), lalu buat deployment baru."
    )

# Pilih storage
MEDIA_STORAGE_BACKEND = (
    "portofolio.storage.SenDevCloudinaryStorage"
    if CLOUDINARY_URL
    else "django.core.files.storage.FileSystemStorage"
)

STORAGES = {
    "default": {
        "BACKEND": MEDIA_STORAGE_BACKEND,
    },
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage."
            "StaticFilesStorage"
        ),
    },
}

# URL media Cloudinary selalu HTTPS
if CLOUDINARY_URL:
    import cloudinary
    cloudinary.config(secure=True)


# =====================================================
# 8. KEAMANAN WEBSITE VERCEL
# =====================================================
SECURE_CONTENT_TYPE_NOSNIFF = True

if IS_VERCEL:
    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https",
    )
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


# =====================================================
# 9. DEFAULT PRIMARY KEY
# =====================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
