#!/usr/bin/env python
"""
Script to verify static files are being collected correctly
Run this on Render to check if CSS file is accessible
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edithclothes.settings')
django.setup()

from django.contrib.staticfiles.finders import find
from django.conf import settings
from pathlib import Path

print("=" * 60)
print("Static Files Diagnostic")
print("=" * 60)

# Check settings
print(f"\nSTATIC_URL: {settings.STATIC_URL}")
print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
print(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
print(f"STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")

# Check if CSS file can be found
css_path = 'admin/css/custom_admin.css'
print(f"\nLooking for: {css_path}")

found_path = find(css_path)
if found_path:
    print(f"✅ Found at: {found_path}")
    # Check if file exists
    if os.path.exists(found_path):
        size = os.path.getsize(found_path)
        print(f"✅ File exists, size: {size} bytes")
    else:
        print(f"❌ File path exists but file not found")
else:
    print(f"❌ File not found by static files finders")
    
# Check staticfiles directory
staticfiles_dir = Path(settings.STATIC_ROOT)
if staticfiles_dir.exists():
    print(f"\n✅ STATIC_ROOT exists: {staticfiles_dir}")
    css_in_staticfiles = staticfiles_dir / 'admin' / 'css' / 'custom_admin.css'
    if css_in_staticfiles.exists():
        print(f"✅ CSS file in staticfiles: {css_in_staticfiles}")
        size = css_in_staticfiles.stat().st_size
        print(f"   Size: {size} bytes")
    else:
        print(f"❌ CSS file NOT in staticfiles directory")
        # List what's in admin/css
        admin_css_dir = staticfiles_dir / 'admin' / 'css'
        if admin_css_dir.exists():
            print(f"   Files in {admin_css_dir}:")
            for f in admin_css_dir.iterdir():
                print(f"     - {f.name}")
        else:
            print(f"   Directory {admin_css_dir} does not exist")
else:
    print(f"\n❌ STATIC_ROOT does not exist: {staticfiles_dir}")

# Check source file
source_file = Path(__file__).parent / 'shop' / 'static' / 'admin' / 'css' / 'custom_admin.css'
if source_file.exists():
    print(f"\n✅ Source file exists: {source_file}")
    size = source_file.stat().st_size
    print(f"   Size: {size} bytes")
else:
    print(f"\n❌ Source file NOT found: {source_file}")

print("\n" + "=" * 60)

