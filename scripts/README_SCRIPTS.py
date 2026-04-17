"""
Nexalith — Backend Admin Scripts
══════════════════════════════════════════════════════
IMPORTANT: These scripts are for LOCAL / DEVELOPMENT use only.
They must NEVER be included in the Docker production build.

Move all of these files here:
  - force_user.py        → backend/scripts/force_user.py
  - reset_passwords.py   → backend/scripts/reset_passwords.py
  - seed_users_fixed.py  → backend/scripts/seed_users_fixed.py
  - list_users.py        → backend/scripts/list_users.py
  - apply_custom_credentials.py → backend/scripts/apply_custom_credentials.py

Then add this to your Dockerfile to exclude scripts from production:
──────────────────────────────────────────────────────
  # In your Dockerfile — copy app but exclude scripts
  COPY . /app
  RUN rm -rf /app/scripts   # ← add this line
──────────────────────────────────────────────────────

Also add /scripts/ to your .gitignore if any script contains
real credentials or seed passwords.

HOW TO RUN THESE SCRIPTS (from project root):
  python scripts/seed_users_fixed.py
  python scripts/list_users.py
"""
