import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medical_billing.settings')
django.setup()

from workflow.models import Job
from django.utils import timezone
from datetime import timedelta
from workflow.views import JobViewSet
from rest_framework.test import APIRequestFactory

factory = APIRequestFactory()
request = factory.get('/api/jobs/stuck_jobs/')

viewset = JobViewSet()
viewset.request = request
viewset.format_kwarg = None

print("Checking stuck_jobs logic...")
try:
    response = viewset.stuck_jobs(request)
    print("Success:", response.data)
except Exception as e:
    import traceback
    print("Error detected:")
    traceback.print_exc()
