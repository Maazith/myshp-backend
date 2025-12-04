#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # Exit on error

echo "🔨 Installing dependencies..."
pip install -r requirements.txt

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Build complete!"

