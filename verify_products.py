#!/usr/bin/env python
"""
Script to verify products exist and are configured correctly
Run: python manage.py shell < verify_products.py
Or: python manage.py shell, then paste this code
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edithclothes.settings')
django.setup()

from shop.models import Product, Category

print("\n" + "="*60)
print("  PRODUCT VERIFICATION")
print("="*60)

# Check all products
all_products = Product.objects.all()
print(f"\n📦 Total Products in Database: {all_products.count()}")

if all_products.count() == 0:
    print("\n⚠️  No products found in database!")
    print("   Create products in admin panel or use management command.")
else:
    print("\n📋 Product Details:")
    print("-" * 60)
    
    for product in all_products:
        print(f"\n  Product ID: {product.id}")
        print(f"  Title: {product.title}")
        print(f"  Gender: {product.gender}")
        print(f"  Base Price: ₹{product.base_price}")
        print(f"  Is Active: {'✅ YES' if product.is_active else '❌ NO'}")
        print(f"  Category: {product.category.name if product.category else 'None'}")
        print(f"  Hero Media: {'✅ Has image' if product.hero_media else '❌ No image'}")
        print(f"  Variants: {product.variants.count()}")
        
        if not product.is_active:
            print(f"  ⚠️  WARNING: Product is INACTIVE - won't show on frontend!")

# Check active products (what API returns)
active_products = Product.objects.filter(is_active=True)
print(f"\n✅ Active Products (will show on frontend): {active_products.count()}")

if active_products.count() == 0 and all_products.count() > 0:
    print("\n⚠️  ISSUE FOUND: Products exist but all are INACTIVE!")
    print("   Solution: Go to admin panel and check 'Is Active' for products.")

# Check by gender
men_products = Product.objects.filter(is_active=True, gender='MEN')
women_products = Product.objects.filter(is_active=True, gender='WOMEN')
unisex_products = Product.objects.filter(is_active=True, gender='UNISEX')

print(f"\n📊 Active Products by Gender:")
print(f"  Men: {men_products.count()}")
print(f"  Women: {women_products.count()}")
print(f"  Unisex: {unisex_products.count()}")

# Check categories
categories = Category.objects.all()
print(f"\n📁 Categories: {categories.count()}")
if categories.count() == 0:
    print("  ⚠️  No categories found - products need a category!")

print("\n" + "="*60)
print("  VERIFICATION COMPLETE")
print("="*60)

