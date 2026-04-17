import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'medical_billing.settings'
django.setup()

from workflow.models import User
from django.contrib.auth import authenticate

print('\n=== USERS IN DATABASE ===')
users = User.objects.all().values('username', 'role', 'is_active', 'user_type')
for u in users:
    print(u)

print('\n=== DB ENGINE ===')
from django.db import connection
print('Using:', connection.vendor)

print('\n=== AUTH TEST ===')
test_cases = [
    ('admin', 'Admin@1234'),
    ('ops_manager', 'OpsManager@1234'),
    ('billing_staff', 'Billing@1234'),
    ('payment_staff', 'Payment@1234'),
    ('ar_staff', 'ARDenial@1234'),
]
for username, password in test_cases:
    result = authenticate(username=username, password=password)
    print(f'{username}: {"PASS" if result else "FAIL"}')
