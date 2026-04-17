from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0002_alter_job_options_alter_user_options'),
    ]

    operations = [
        migrations.RunSQL(
            "CREATE EXTENSION IF NOT EXISTS pgcrypto;",
            reverse_sql="DROP EXTENSION IF EXISTS pgcrypto;"
        )
    ]
