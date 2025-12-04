#!/usr/bin/env bash
# Startup script that runs migrations automatically

set -o errexit

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📁 Current directory: $(pwd)"
echo "📦 Python version: $(python --version)"
echo "📦 Python path: $(which python)"
echo "📦 Django version: $(python -c 'import django; print(django.get_version())' 2>/dev/null || echo 'Django not found')"

# Verify manage.py exists
if [ ! -f "manage.py" ]; then
    echo "❌ ERROR: manage.py not found in $(pwd)"
    echo "📂 Listing directory contents:"
    ls -la
    exit 1
fi

# Verify edithclothes module exists
if [ ! -d "edithclothes" ]; then
    echo "❌ ERROR: edithclothes module not found in $(pwd)"
    echo "📂 Listing directory contents:"
    ls -la
    exit 1
fi

echo "✅ Found manage.py and edithclothes module"

echo "🔄 Running database migrations..."
python manage.py migrate --noinput

echo "✅ Migrations complete!"

# Create superuser from environment variables if provided
echo "👤 Checking for superuser creation..."
python manage.py create_superuser_from_env || echo "⚠️  Superuser creation skipped (set DJANGO_SUPERUSER_* env vars to auto-create)"

echo "🚀 Starting Gunicorn..."

# Enable Django logging to see errors
export PYTHONUNBUFFERED=1

# Start Gunicorn - make sure we're using the correct module path
echo "📍 Gunicorn command: gunicorn edithclothes.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120 --log-level debug --access-logfile - --error-logfile -"
exec gunicorn edithclothes.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120 --log-level debug --access-logfile - --error-logfile -

