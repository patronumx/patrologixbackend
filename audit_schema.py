import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medical_billing.settings')
django.setup()

def audit_schema():
    with connection.cursor() as cursor:
        cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'workflow_job' AND column_name IN ('patient_name', 'patient_id', 'insurance_provider')")
        results = cursor.fetchall()
        print("Schema Audit Results:")
        for col, dtype in results:
            print(f"Column: {col}, Type: {dtype}")

if __name__ == "__main__":
    audit_schema()
