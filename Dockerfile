# Base Python image
FROM python:3.12-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create non-root user
RUN adduser --disabled-password appuser
USER appuser

# Expose port
EXPOSE 8000

# Start server:
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]