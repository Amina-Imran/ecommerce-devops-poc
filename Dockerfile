# Use lightweight Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DEFAULT_TIMEOUT=100

# Set work directory
WORKDIR /app

# Install system dependencies (needed for psycopg2 and others)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt /app/

# Upgrade pip and install requirements
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -i https://pypi.org/simple -r requirements.txt

# Copy project files
COPY . /app/

# Collect static files (skip errors if STATICFILES_DIRS not set)
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8000

# Replace "ecommerce" with your inner project folder name if it's different
CMD ["gunicorn", "--chdir", "ecommerce", "ecommerce.wsgi:application", "--bind", "0.0.0.0:8000"]
