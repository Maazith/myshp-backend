#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # Exit on error

echo "🔨 Installing dependencies..."
pip install -r requirements.txt

echo "📦 Collecting static files..."
# Ensure staticfiles directory exists
mkdir -p staticfiles

# Collect static files - use --clear to ensure clean collection
python manage.py collectstatic --noinput --clear

echo "📋 Verifying static files collection..."
# Check if staticfiles directory was created and has content
if [ -d "staticfiles" ]; then
    echo "✅ staticfiles directory exists"
    file_count=$(find staticfiles -type f | wc -l)
    echo "   Found $file_count static files"
else
    echo "❌ staticfiles directory was not created"
    exit 1
fi

# Check if critical static files exist
if [ -f "staticfiles/admin/css/custom_admin.css" ]; then
    css_size=$(stat -f%z "staticfiles/admin/css/custom_admin.css" 2>/dev/null || stat -c%s "staticfiles/admin/css/custom_admin.css" 2>/dev/null || echo "unknown")
    echo "✅ Custom admin CSS found in staticfiles (size: $css_size bytes)"
elif [ -f "shop/static/admin/css/custom_admin.css" ]; then
    echo "⚠️  Custom admin CSS found in source but not in staticfiles"
    echo "   Attempting to copy manually..."
    mkdir -p staticfiles/admin/css
    cp shop/static/admin/css/custom_admin.css staticfiles/admin/css/custom_admin.css
    echo "✅ CSS file copied to staticfiles"
else
    echo "❌ Custom admin CSS not found anywhere"
    exit 1
fi

echo "✅ Build complete!"

