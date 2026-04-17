"""
Nexalith — Async Tasks (Celery)
All long-running billing operations go here.
Never run these synchronously in views — always call .delay() or .apply_async()
"""
import logging
from celery import shared_task

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# CLAIM SUBMISSION
# ─────────────────────────────────────────────

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def submit_claim_async(self, claim_id: int):
    """
    Submit a single claim to the payer asynchronously.
    Usage in views: submit_claim_async.delay(claim.id)
    """
    try:
        from workflow.models import Claim  # adjust import to your actual model
        claim = Claim.objects.get(id=claim_id)
        claim.status = "submitting"
        claim.save(update_fields=["status"])

        # TODO: Replace with your actual payer API call
        # response = payer_api.submit(claim)
        # claim.status = "submitted" if response.ok else "failed"

        claim.status = "submitted"
        claim.save(update_fields=["status"])
        logger.info(f"Claim {claim_id} submitted successfully.")
        return {"claim_id": claim_id, "status": "submitted"}

    except Exception as exc:
        logger.error(f"Claim {claim_id} submission failed: {exc}")
        raise self.retry(exc=exc)


# ─────────────────────────────────────────────
# ELIGIBILITY VERIFICATION
# ─────────────────────────────────────────────

@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def verify_eligibility_async(self, patient_id: int, payer_id: str):
    """
    Run insurance eligibility check asynchronously.
    Usage: verify_eligibility_async.delay(patient.id, "BCBS")
    """
    try:
        # TODO: Replace with your actual eligibility API call
        # result = eligibility_api.check(patient_id, payer_id)
        result = {"eligible": True, "copay": 20, "deductible_met": False}
        logger.info(f"Eligibility verified for patient {patient_id}: {result}")
        return result

    except Exception as exc:
        logger.error(f"Eligibility check failed for patient {patient_id}: {exc}")
        raise self.retry(exc=exc)


# ─────────────────────────────────────────────
# DENIAL PROCESSING
# ─────────────────────────────────────────────

@shared_task(bind=True, max_retries=2, default_retry_delay=120)
def process_denial_async(self, claim_id: int, denial_reason: str):
    """
    Process a denied claim — log it, flag for follow-up.
    Usage: process_denial_async.delay(claim.id, "CO-4")
    """
    try:
        from workflow.models import Claim, DenialLog  # adjust to your models
        claim = Claim.objects.get(id=claim_id)
        claim.status = "denied"
        claim.save(update_fields=["status"])

        DenialLog.objects.create(
            claim=claim,
            reason_code=denial_reason,
            requires_followup=True,
        )

        logger.warning(f"Claim {claim_id} denied. Reason: {denial_reason}. Flagged for follow-up.")
        return {"claim_id": claim_id, "denial_reason": denial_reason}

    except Exception as exc:
        logger.error(f"Denial processing failed for claim {claim_id}: {exc}")
        raise self.retry(exc=exc)


# ─────────────────────────────────────────────
# BATCH CLAIM SUBMISSION
# ─────────────────────────────────────────────

@shared_task
def submit_batch_claims_async(claim_ids: list):
    """
    Submit a batch of claims — fires individual tasks for each.
    Usage: submit_batch_claims_async.delay([1, 2, 3, 4, 5])
    """
    results = []
    for claim_id in claim_ids:
        task = submit_claim_async.delay(claim_id)
        results.append({"claim_id": claim_id, "task_id": task.id})
    logger.info(f"Batch submitted {len(claim_ids)} claims.")
    return results


# ─────────────────────────────────────────────
# A/R AGING REPORT (runs nightly via Celery Beat)
# ─────────────────────────────────────────────

@shared_task
def generate_ar_aging_report():
    """
    Scheduled task: generate A/R aging report every night at midnight.
    Add to CELERY_BEAT_SCHEDULE in settings.py (see settings patch).
    """
    from django.utils import timezone
    from datetime import timedelta

    today = timezone.now().date()
    buckets = {
        "0_30": 0, "31_60": 0,
        "61_90": 0, "91_120": 0, "120_plus": 0
    }

    # TODO: Replace with your actual AR model queries
    # claims = Claim.objects.filter(status="unpaid")
    # for claim in claims:
    #     age = (today - claim.service_date).days
    #     if age <= 30: buckets["0_30"] += claim.amount
    #     elif age <= 60: buckets["31_60"] += claim.amount
    #     ... etc

    logger.info(f"A/R aging report generated for {today}: {buckets}")
    return buckets
