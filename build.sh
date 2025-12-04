#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # Exit on error

echo "🔨 Installing dependencies..."
pip install -r requirements.txt

echo "📦 Collecting static files..."
# Collect static files - continue even if some files fail
python manage.py collectstatic --noinput || echo "⚠️  Some static files may not have been collected"

echo "📋 Verifying static files collection..."
# Check if critical static files exist
if [ -f "staticfiles/admin/css/custom_admin.css" ] || [ -f "shop/static/admin/css/custom_admin.css" ]; then
    echo "✅ Custom admin CSS found"
else
    echo "⚠️  Custom admin CSS not found - admin will use default styles"
fi

echo "✅ Build complete!"

