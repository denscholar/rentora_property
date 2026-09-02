# ---- Base image ----
FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# libpq-dev is enough for psycopg2-binary at runtime — no build-essential/gcc needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---- Install Python deps first (layer caching) ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy project code ----
COPY . .

# Dummy values so settings.py can import during the build.
# collectstatic never reads these values, it just needs Django to load without crashing.
# Real values are supplied at runtime via .env — these build-time ones are never used by the running app.
ENV SECRET_KEY=build-time-placeholder-not-used-at-runtime \
    DEBUG=False \
    ALLOWED_HOSTS=localhost \
    DB_NAME=placeholder \
    DB_USER=placeholder \
    DB_PASSWORD=placeholder \
    DB_HOST=placeholder \
    DB_PORT=5432 \
    CLOUDINARY_CLOUD_NAME=placeholder \
    CLOUDINARY_API_KEY=placeholder \
    CLOUDINARY_API_SECRET=placeholder \
    CLOUDINARY_SECURE=True \
    RESEND_API_KEY=placeholder \
    RESEND_FROM_EMAIL=placeholder \
    FRONTEND_URL=http://localhost \
    PROPERTY_VERIFICATION_URL=http://localhost

# Collect static files (frontend JS/CSS/templates included)
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# ---- Run with gunicorn ----
CMD ["gunicorn", "api.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "60"]