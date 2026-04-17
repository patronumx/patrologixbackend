# Nexalith Backend — Production Dockerfile
# ══════════════════════════════════════════
# Replaces your existing Dockerfile in nexusbackend/

FROM python:3.12-alpine

# System dependencies
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    curl \
    python3-dev \
    libffi-dev

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# ─── SECURITY: Remove dev-only admin scripts from production image ───
RUN rm -rf /app/scripts \
    /app/force_user.py \
    /app/reset_passwords.py \
    /app/seed_users_fixed.py \
    /app/list_users.py \
    /app/apply_custom_credentials.py \
    /app/test_login.py \
    /app/test_login_std.py \
    /app/test_ops_login.py \
    /app/test_ops_login_std.py

# Create logs directory for HIPAA audit logs
RUN mkdir -p /app/logs

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health/ || exit 1

# Start gunicorn (runs migrations, user setup, and celery automatically for Render free tier)
CMD sh -c "python manage.py migrate && python create_users.py && celery -A medical_billing worker --loglevel=info --concurrency=2 & gunicorn medical_billing.wsgi:application \
     --bind 0.0.0.0:8000 \
     --workers 4 \
     --threads 2 \
     --timeout 120 \
     --access-logfile - \
     --error-logfile -"
