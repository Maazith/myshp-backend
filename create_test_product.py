#!/usr/bin/env python
"""
Create a test product for homepage verification
Run: python manage.py shell < create_test_product.py
Or: python manage.py shell, then paste this code
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edithclothes.settings')
django.setup()

from shop.models import Product, Category

print("\n" + "="*60)
print("  CREATE TEST PRODUCT")
print("="*60)

# Get or create a category
category, created = Category.objects.get_or_create(
    name='Test Category',
    defaults={'description': 'Test category for products'}
)
if created:
    print(f"✅ Created category: {category.name}")
else:
    print(f"✅ Using existing category: {category.name}")

# Check if test product already exists
existing = Product.objects.filter(title='Test Product').first()
if existing:
    print(f"\n⚠️  Test product already exists (ID: {existing.id})")
    print("   Updating existing product...")
    product = existing
else:
    print("\n📦 Creating new test product...")
    product = Product()

# Set product fields
product.title = 'Test Product'
product.category = category
product.base_price = 500.00
product.gender = 'MEN'
product.description = 'This is a test product created to verify homepage display.'
product.is_active = True
product.is_featured = False

product.save()

print(f"\n✅ Product created/updated:")
print(f"   ID: {product.id}")
print(f"   Title: {product.title}")
print(f"   Gender: {product.gender}")
print(f"   Price: ₹{product.base_price}")
print(f"   Is Active: {product.is_active}")
print(f"   Category: {product.category.name}")

# Create default variant if none exist
if product.variants.count() == 0:
    from shop.models import ProductVariant
    variant = ProductVariant.objects.create(
        product=product,
        size='M',
        color='Black',
        stock=10
    )
    print(f"\n✅ Created default variant: {variant.size}/{variant.color}")

print("\n" + "="*60)
print("  NEXT STEPS")
print("="*60)
print("1. Test API: https://myshp-backend.onrender.com/api/products/")
print("2. Check homepage: https://myshp-frontend.vercel.app/")
print("3. Product should appear on Men's page")
print("="*60)

