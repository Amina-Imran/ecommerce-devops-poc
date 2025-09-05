# Use lightweight Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DEFAULT_TIMEOUT=100

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files (this already includes db.sqlite3 + products.json if present)
COPY . /app/

# Switch into Django project folder
WORKDIR /app/ecommerce

# Collect static files at build time
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8000

# At runtime → migrate, load products, then start Gunicorn
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py loaddata /app/products.json || true && gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000"]
