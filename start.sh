#!/usr/bin/env bash
# Startup script that runs migrations automatically

set -o errexit
set -o pipefail

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 Starting Django application..."
echo "📁 Current directory: $(pwd)"
echo "📦 Python version: $(python --version)"
echo "📦 Python path: $(which python)"

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

# Check Django installation
DJANGO_VERSION=$(python -c 'import django; print(django.get_version())' 2>/dev/null || echo 'Django not found')
echo "📦 Django version: $DJANGO_VERSION"

# Verify PORT is set (Render sets this automatically)
if [ -z "$PORT" ]; then
    echo "⚠️  WARNING: PORT environment variable not set, defaulting to 10000"
    export PORT=10000
fi
echo "🌐 Using PORT: $PORT"

# Check database connection
echo "🔍 Checking database connection..."
python manage.py check --database default || {
    echo "⚠️  Database check failed, but continuing..."
}

# Run migrations
echo "🔄 Running database migrations..."
python manage.py migrate --noinput || {
    echo "❌ ERROR: Migrations failed"
    exit 1
}
echo "✅ Migrations complete!"

# Ensure admin user exists (create or reset if needed)
echo "👤 Ensuring admin user exists..."
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "📋 Admin credentials provided, creating/updating admin user..."
    python manage.py ensure_admin_user --reset || echo "⚠️  Admin user creation skipped (may already exist)"
else
    echo "⚠️  Admin credentials not provided, skipping admin user creation"
    echo "   Set DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, and DJANGO_SUPERUSER_PASSWORD to create admin user"
fi

# Enable Django logging to see errors
export PYTHONUNBUFFERED=1

# Start Gunicorn
echo "🚀 Starting Gunicorn server..."
echo "📍 Gunicorn command: gunicorn edithclothes.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --log-level info --access-logfile - --error-logfile - --preload"

# Use preload for better performance, 2 workers for starter plan
exec gunicorn edithclothes.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --log-level info \
    --access-logfile - \
    --error-logfile - \
    --preload

