"""
Nexalith — HIPAA Audit Trail
══════════════════════════════════════════════════════
Register any model that touches PHI (Protected Health Info)
with auditlog so every create/update/delete is logged.

HOW TO USE:
  1. pip install django-auditlog
  2. Add 'auditlog' to INSTALLED_APPS
  3. Run: python manage.py migrate
  4. Import AuditlogHistoryField + register() in your models.py

══════════════════════════════════════════════════════
"""

from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField
from django.db import models


# ─────────────────────────────────────────────
# MIXIN: Add to any model that handles PHI
# ─────────────────────────────────────────────

class HIPAAAuditMixin(models.Model):
    """
    Add this mixin to any model that stores PHI.
    It adds a history field and auto-registers with auditlog.

    Usage:
        class Claim(HIPAAAuditMixin, models.Model):
            patient_name = models.CharField(max_length=255)
            ...
    """
    history = AuditlogHistoryField()

    class Meta:
        abstract = True


# ─────────────────────────────────────────────
# EXAMPLE: How to register your existing models
# Add these lines to the BOTTOM of your models.py files
# ─────────────────────────────────────────────

# from auditlog.registry import auditlog
# from .models import Claim, Patient, Payment, EligibilityCheck
#
# auditlog.register(Claim)
# auditlog.register(Patient)
# auditlog.register(Payment)
# auditlog.register(EligibilityCheck)


# ─────────────────────────────────────────────
# AUDIT MIDDLEWARE: Log every API request with user info
# Add 'medical_billing.audit_middleware.HIPAARequestMiddleware'
# to your MIDDLEWARE list in settings.py (after auth middleware)
# ─────────────────────────────────────────────

import logging
import json

audit_logger = logging.getLogger("auditlog")


class HIPAARequestMiddleware:
    """
    Logs every API request that touches PHI-related endpoints.
    Add to settings.py MIDDLEWARE list.
    """
    PHI_ENDPOINTS = ["/api/claims", "/api/patients", "/api/payments", "/api/eligibility"]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Only log PHI-related endpoints
        if any(request.path.startswith(ep) for ep in self.PHI_ENDPOINTS):
            user = request.user.username if request.user.is_authenticated else "anonymous"
            audit_logger.info(
                f"PHI_ACCESS | user={user} | method={request.method} "
                f"| path={request.path} | status={response.status_code} "
                f"| ip={self.get_client_ip(request)}"
            )

        return response

    def get_client_ip(self, request):
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "unknown")
