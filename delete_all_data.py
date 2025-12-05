"""
Script to delete all products and banners from the database.
Run this from Django shell: python manage.py shell < delete_all_data.py
Or run interactively: python manage.py shell, then copy-paste the commands below.
"""

from shop.models import Product, Banner

# Delete all products (this will cascade delete variants, images, etc.)
products_count = Product.objects.count()
Product.objects.all().delete()
print(f"✅ Deleted {products_count} product(s)")

# Delete all banners
banners_count = Banner.objects.count()
Banner.objects.all().delete()
print(f"✅ Deleted {banners_count} banner(s)")

print("\n🎉 All products and banners have been deleted!")

