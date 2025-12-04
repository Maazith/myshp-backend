#!/usr/bin/env bash
# Startup script that runs migrations automatically

set -o errexit

echo "🔄 Running database migrations..."
python manage.py migrate --noinput

echo "✅ Migrations complete!"
echo "🚀 Starting Gunicorn..."

# Start Gunicorn
exec gunicorn edithclothes.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120

