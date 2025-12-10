#!/usr/bin/env python
"""
Deployment Verification Script for Render
Tests all critical endpoints and configurations
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edithclothes.settings')
django.setup()

from django.test import Client
from django.conf import settings
from django.contrib.auth.models import User
from shop.models import Product, Order

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def check_settings():
    """Verify Django settings are correct"""
    print_section("Django Settings Check")
    
    checks = {
        "DEBUG": settings.DEBUG,
        "ALLOWED_HOSTS": settings.ALLOWED_HOSTS,
        "DATABASE": settings.DATABASES['default']['ENGINE'],
        "STATIC_ROOT": str(settings.STATIC_ROOT),
        "MEDIA_ROOT": str(settings.MEDIA_ROOT),
        "CORS_ALLOWED_ORIGINS": settings.CORS_ALLOWED_ORIGINS if hasattr(settings, 'CORS_ALLOWED_ORIGINS') else "N/A",
    }
    
    for key, value in checks.items():
        status = "✅" if value else "❌"
        print(f"{status} {key}: {value}")
    
    # Check if DEBUG is False in production
    if settings.DEBUG:
        print("⚠️  WARNING: DEBUG is True in production!")
    else:
        print("✅ DEBUG is False (production mode)")

def check_database():
    """Verify database connection and migrations"""
    print_section("Database Check")
    
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    
    # Check if migrations are applied
    try:
        from django.core.management import call_command
        from io import StringIO
        out = StringIO()
        call_command('showmigrations', '--plan', stdout=out)
        migrations = out.getvalue()
        if '[X]' in migrations:
            print("✅ Migrations are applied")
        else:
            print("⚠️  No migrations found or not applied")
    except Exception as e:
        print(f"⚠️  Could not check migrations: {e}")
    
    return True

def check_static_files():
    """Verify static files are collected"""
    print_section("Static Files Check")
    
    static_root = settings.STATIC_ROOT
    if os.path.exists(static_root):
        file_count = len([f for f in os.listdir(static_root) if os.path.isfile(os.path.join(static_root, f))])
        print(f"✅ Static files directory exists with {file_count} files")
        
        # Check for admin static files
        admin_css = os.path.join(static_root, 'admin', 'css')
        if os.path.exists(admin_css):
            print("✅ Admin CSS files found")
        else:
            print("⚠️  Admin CSS files not found")
    else:
        print(f"❌ Static files directory not found: {static_root}")

def check_endpoints():
    """Test critical API endpoints"""
    print_section("API Endpoints Check")
    
    client = Client()
    
    endpoints = [
        ('/', 'Root endpoint'),
        ('/api/', 'API root'),
        ('/api/products/', 'Products list'),
        ('/api/categories/', 'Categories list'),
        ('/api/banners/', 'Banners list'),
    ]
    
    for endpoint, description in endpoints:
        try:
            response = client.get(endpoint)
            status = "✅" if response.status_code in [200, 401, 403] else "❌"
            print(f"{status} {description} ({endpoint}): {response.status_code}")
        except Exception as e:
            print(f"❌ {description} ({endpoint}): Error - {e}")

def check_admin():
    """Verify admin panel is accessible"""
    print_section("Admin Panel Check")
    
    client = Client()
    
    try:
        response = client.get('/edith-admin-login/')
        if response.status_code == 200:
            print("✅ Admin panel is accessible")
        elif response.status_code == 302:
            print("✅ Admin panel redirects to login (expected)")
        else:
            print(f"⚠️  Admin panel returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Admin panel check failed: {e}")

def check_models():
    """Verify models are working"""
    print_section("Models Check")
    
    try:
        product_count = Product.objects.count()
        print(f"✅ Products model: {product_count} products")
    except Exception as e:
        print(f"❌ Products model error: {e}")
    
    try:
        user_count = User.objects.count()
        print(f"✅ Users model: {user_count} users")
    except Exception as e:
        print(f"❌ Users model error: {e}")

def main():
    """Run all verification checks"""
    print("\n" + "="*60)
    print("  RENDER DEPLOYMENT VERIFICATION")
    print("="*60)
    
    check_settings()
    if check_database():
        check_models()
    check_static_files()
    check_endpoints()
    check_admin()
    
    print_section("Verification Complete")
    print("✅ All critical checks completed!")
    print("\nIf any checks failed, review the errors above.")
    print("For deployment issues, check Render logs and environment variables.")

if __name__ == '__main__':
    main()

