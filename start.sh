#!/usr/bin/env bash
# Startup script that runs migrations automatically

set -o errexit

# Change to the directory where this script is located (backend directory)
cd "$(dirname "$0")"

echo "📁 Current directory: $(pwd)"
echo "📦 Python version: $(python --version)"
echo "📦 Django version: $(python -c 'import django; print(django.get_version())')"

echo "🔄 Running database migrations..."
python manage.py migrate --noinput

echo "✅ Migrations complete!"
echo "🚀 Starting Gunicorn..."

# Start Gunicorn - make sure we're using the correct module path
exec gunicorn edithclothes.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120 --chdir .

