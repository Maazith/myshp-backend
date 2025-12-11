"""
Script to completely delete all products, banners, and related data.
Run: python manage.py shell < clear_all_products.py
"""

from shop.models import Product, Banner, ProductVariant, ProductImage, CartItem, OrderItem
import os
import shutil
from django.conf import settings

# Delete from database
products_count = Product.objects.count()
variants_count = ProductVariant.objects.count()
images_count = ProductImage.objects.count()
banners_count = Banner.objects.count()
cart_items_count = CartItem.objects.count()
order_items_count = OrderItem.objects.count()

# Delete all related data
Product.objects.all().delete()
Banner.objects.all().delete()
ProductVariant.objects.all().delete()
ProductImage.objects.all().delete()
CartItem.objects.all().delete()
OrderItem.objects.all().delete()

print(f"✅ Deleted from database:")
print(f"   - {products_count} product(s)")
print(f"   - {variants_count} variant(s)")
print(f"   - {images_count} product image(s)")
print(f"   - {banners_count} banner(s)")
print(f"   - {cart_items_count} cart item(s)")
print(f"   - {order_items_count} order item(s)")

# Delete media files
deleted_files = 0
deleted_dirs = 0

# Delete product images
products_dir = os.path.join(settings.MEDIA_ROOT, 'products')
if os.path.exists(products_dir):
    for item in os.listdir(products_dir):
        item_path = os.path.join(products_dir, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
            deleted_files += 1
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
            deleted_dirs += 1

# Delete banner images
banners_dir = os.path.join(settings.MEDIA_ROOT, 'banners')
if os.path.exists(banners_dir):
    for item in os.listdir(banners_dir):
        item_path = os.path.join(banners_dir, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
            deleted_files += 1

print(f"\n✅ Deleted from media:")
print(f"   - {deleted_files} image file(s)")
print(f"   - {deleted_dirs} directory/directories")

# Verify deletion
print(f"\n📊 Verification:")
print(f"   - Products: {Product.objects.count()}")
print(f"   - Variants: {ProductVariant.objects.count()}")
print(f"   - Product Images: {ProductImage.objects.count()}")
print(f"   - Banners: {Banner.objects.count()}")
print(f"   - Cart Items: {CartItem.objects.count()}")
print(f"   - Order Items: {OrderItem.objects.count()}")

print("\n🎉 All products, banners, and images have been completely deleted!")

