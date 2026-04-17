import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medical_billing.settings')
django.setup()

from workflow.models import User

users = [
    {
        "username": "admin",
        "password": "Admin@1234",
        "full_name": "System Administrator",
        "role": "admin",
        "user_type": "admin",
        "is_staff": True,
        "is_superuser": True,
    },
    {
        "username": "ops_manager",
        "password": "OpsManager@1234",
        "full_name": "Operations Manager",
        "role": "operations_manager",
        "user_type": "employee",
        "is_staff": False,
        "is_superuser": False,
    },
    {
        "username": "billing_staff",
        "password": "Billing@1234",
        "full_name": "Billing Staff",
        "role": "billing",
        "user_type": "employee",
        "is_staff": False,
        "is_superuser": False,
    },
    {
        "username": "payment_staff",
        "password": "Payment@1234",
        "full_name": "Payment Posting Staff",
        "role": "payment",
        "user_type": "employee",
        "is_staff": False,
        "is_superuser": False,
    },
    {
        "username": "ar_staff",
        "password": "ARDenial@1234",
        "full_name": "AR / Denial Staff",
        "role": "ar_denial",
        "user_type": "employee",
        "is_staff": False,
        "is_superuser": False,
    },
]

print("\n" + "="*55)
print("  NEXALITH — USER SEED SCRIPT")
print("="*55)

for u in users:
    obj, created = User.objects.get_or_create(username=u["username"])
    obj.set_password(u["password"])
    obj.full_name = u["full_name"]
    obj.role = u["role"]
    obj.user_type = u["user_type"]
    obj.is_staff = u["is_staff"]
    obj.is_superuser = u["is_superuser"]
    obj.save()
    status = "CREATED" if created else "UPDATED"
    print(f"  [{status}] {u['username']} | role={u['role']}")

print("="*55)
print("  All users ready.")
print("="*55 + "\n")
