import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medical_billing.settings')
django.setup()

def enable_pgcrypto():
    with connection.cursor() as cursor:
        print("Enabling pgcrypto extension...")
        try:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")
            print("Extension pgcrypto enabled successfully.")
        except Exception as e:
            print(f"Error enabling extension: {e}")

if __name__ == "__main__":
    enable_pgcrypto()
