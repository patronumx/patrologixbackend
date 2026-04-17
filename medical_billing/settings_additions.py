"""
Nexalith — Settings Additions
═══════════════════════════════════════════════════════
PASTE THESE BLOCKS INTO YOUR EXISTING settings.py
Do NOT replace your whole settings.py — add each block.
═══════════════════════════════════════════════════════
"""

# ─────────────────────────────────────────────
# 1. ADD TO INSTALLED_APPS
# ─────────────────────────────────────────────
INSTALLED_APPS = [
    # ... your existing apps ...
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    "auditlog",           # ← ADD: HIPAA audit trail
    "django_ratelimit",   # ← ADD: API rate limiting
]


# ─────────────────────────────────────────────
# 2. CELERY + REDIS CONFIG (async task queue)
# ─────────────────────────────────────────────
import os

CELERY_BROKER_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 min max per task

# Scheduled tasks (Celery Beat) — runs nightly A/R aging report
from celery.schedules import crontab
CELERY_BEAT_SCHEDULE = {
    "ar-aging-report-nightly": {
        "task": "workflow.tasks.generate_ar_aging_report",
        "schedule": crontab(hour=0, minute=0),  # midnight UTC every night
    },
}


# ─────────────────────────────────────────────
# 3. HIPAA AUDIT LOGGING
# ─────────────────────────────────────────────
AUDITLOG_INCLUDE_ALL_MODELS = False  # Only log models you register explicitly

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "hipaa": {
            "format": "[HIPAA AUDIT] {asctime} | user={name} | action={message}",
            "style": "{",
        },
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "hipaa_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/hipaa_audit.log",
            "maxBytes": 10 * 1024 * 1024,  # 10MB per file
            "backupCount": 10,              # keep 10 files = 100MB of audit history
            "formatter": "hipaa",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "auditlog": {
            "handlers": ["hipaa_file"],
            "level": "INFO",
            "propagate": False,
        },
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}

# Make sure this directory exists — add to your Dockerfile/setup:
# RUN mkdir -p /app/logs


# ─────────────────────────────────────────────
# 4. SECURITY SETTINGS (HIPAA + general hardening)
# ─────────────────────────────────────────────

# Force HTTPS in production
SECURE_SSL_REDIRECT = os.environ.get("DJANGO_ENV") == "production"
SECURE_HSTS_SECONDS = 31536000           # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"

# Session timeout — HIPAA recommends auto-logout after inactivity
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


# ─────────────────────────────────────────────
# 5. JWT SETTINGS (tighten up token lifetimes)
# ─────────────────────────────────────────────
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),  # Short-lived for HIPAA
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "AUTH_HEADER_TYPES": ("Bearer",),
}


# ─────────────────────────────────────────────
# 6. DJANGO REST FRAMEWORK — add throttling
# ─────────────────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "20/hour",       # 20 requests/hour for unauthenticated
        "user": "1000/hour",     # 1000 requests/hour per authenticated user
        "login": "5/minute",     # Tight limit on auth endpoints
    },
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
}
