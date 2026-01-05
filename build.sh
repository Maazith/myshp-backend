#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # Exit on error
set -o pipefail # Exit on pipe failure

echo "🔨 Starting build process..."
echo "📦 Python version: $(python --version)"
echo "📦 Pip version: $(pip --version)"

# Verify Python version matches runtime.txt (3.11.9)
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo "🔍 Detected Python version: $PYTHON_VERSION"
if [[ ! "$PYTHON_VERSION" == "3.11"* ]]; then
    echo "⚠️  WARNING: Python version is not 3.11.x (found $PYTHON_VERSION)"
    echo "   psycopg2-binary may have compatibility issues with newer Python versions"
fi

# Upgrade pip to latest version
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet

# Install system dependencies for psycopg2 (if needed)
echo "📥 Installing system dependencies for PostgreSQL..."
# psycopg2-binary should work without system deps, but ensure pip is up to date

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# CRITICAL: Explicitly install psycopg3 (psycopg) for Python 3.13 compatibility
echo "🔍 Installing PostgreSQL adapter (psycopg3)..."
pip install --no-cache-dir "psycopg[binary]==3.3.2" || {
    echo "⚠️  Standard install failed, trying alternative..."
    pip install --no-cache-dir --upgrade pip setuptools wheel
    pip install --no-cache-dir "psycopg[binary]==3.3.2"
}

# Verify psycopg3 installation
echo "🔍 Verifying psycopg3 installation..."
python -c "import psycopg; print(f'✅ psycopg {psycopg.__version__} installed successfully')" || {
    echo "❌ ERROR: psycopg3 installation failed"
    echo "📦 Attempting to install psycopg2-binary as fallback..."
    pip install --no-cache-dir psycopg2-binary==2.9.9 || {
        echo "❌ ERROR: Both psycopg3 and psycopg2-binary installation failed"
        exit 1
    }
}

# Verify critical packages
echo "✅ Verifying critical packages..."
python -c "import django; print(f'Django {django.get_version()}')" || exit 1
python -c "import rest_framework; print('DRF installed')" || exit 1
python -c "import gunicorn; print('Gunicorn installed')" || exit 1
python -c "import whitenoise; print('WhiteNoise installed')" || exit 1
python -c "import PIL; print('Pillow installed')" || exit 1

# CRITICAL: Verify PostgreSQL adapter installation (psycopg3 for Python 3.13+)
echo "🔍 Verifying PostgreSQL adapter (psycopg)..."
python -c "import psycopg; print(f'psycopg {psycopg.__version__} installed')" || {
    echo "❌ ERROR: psycopg not installed correctly"
    echo "📦 Attempting to reinstall psycopg..."
    pip install --force-reinstall --no-cache-dir "psycopg[binary]==3.3.2" || exit 1
    python -c "import psycopg; print(f'psycopg {psycopg.__version__} installed')" || {
        echo "❌ ERROR: psycopg installation failed"
        exit 1
    }
}
echo "✅ PostgreSQL adapter verified!"

# Ensure staticfiles directory exists
echo "📁 Creating staticfiles directory..."
mkdir -p staticfiles

# Collect static files - use --clear to ensure clean collection
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput --clear || {
    echo "⚠️  Static files collection had warnings, but continuing..."
}

# Verify static files collection
echo "📋 Verifying static files collection..."
if [ -d "staticfiles" ]; then
    file_count=$(find staticfiles -type f 2>/dev/null | wc -l)
    echo "✅ staticfiles directory exists with $file_count files"
    
    # Check for admin static files
    if [ -d "staticfiles/admin" ]; then
        echo "✅ Admin static files collected"
    else
        echo "⚠️  Admin static files not found, but continuing..."
    fi
else
    echo "❌ ERROR: staticfiles directory was not created"
    exit 1
fi

# Check if critical static files exist (non-blocking)
if [ -f "staticfiles/admin/css/custom_admin.css" ]; then
    echo "✅ Custom admin CSS found in staticfiles"
elif [ -f "shop/static/admin/css/custom_admin.css" ]; then
    echo "⚠️  Custom admin CSS found in source but not in staticfiles"
    echo "   Attempting to copy manually..."
    mkdir -p staticfiles/admin/css
    cp shop/static/admin/css/custom_admin.css staticfiles/admin/css/custom_admin.css 2>/dev/null || echo "⚠️  Could not copy CSS, but continuing..."
else
    echo "⚠️  Custom admin CSS not found, but continuing (may use default styles)"
fi

# Ensure media directories exist
echo "📁 Creating media directories..."
mkdir -p media/products media/banners media/payments || echo "⚠️  Could not create media directories, but continuing..."

echo "✅ Build complete!"

