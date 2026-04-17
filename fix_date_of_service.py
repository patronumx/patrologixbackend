import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medical_billing.settings')
django.setup()

def fix_date_of_service():
    with connection.cursor() as cursor:
        print("Migrating date_of_service to bytea...")
        try:
            cursor.execute("""
                ALTER TABLE workflow_job 
                ALTER COLUMN date_of_service TYPE bytea USING date_of_service::text::bytea;
            """)
            print("Successfully migrated date_of_service to bytea.")
        except Exception as e:
            print(f"Error altering date_of_service: {e}")

if __name__ == "__main__":
    fix_date_of_service()
