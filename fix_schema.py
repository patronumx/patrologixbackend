import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medical_billing.settings')
django.setup()

def fix_schema():
    with connection.cursor() as cursor:
        print("Migrating columns to bytea...")
        try:
            cursor.execute("""
                ALTER TABLE workflow_job 
                ALTER COLUMN patient_name TYPE bytea USING patient_name::bytea,
                ALTER COLUMN patient_id TYPE bytea USING patient_id::bytea,
                ALTER COLUMN insurance_provider TYPE bytea USING insurance_provider::bytea;
            """)
            print("Successfully migrated columns to bytea.")
        except Exception as e:
            print(f"Error altering columns: {e}")

if __name__ == "__main__":
    fix_schema()
