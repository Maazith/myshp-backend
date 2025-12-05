# How to Delete All Products and Banners Manually

## Method 1: Using Django Shell (Recommended)

### Option A: Interactive Shell

1. Open terminal/command prompt in the `backend` directory
2. Run:
   ```bash
   python manage.py shell
   ```
3. Copy and paste these commands:
   ```python
   from shop.models import Product, Banner
   
   # Delete all products (cascades to variants, images, etc.)
   products_count = Product.objects.count()
   Product.objects.all().delete()
   print(f"✅ Deleted {products_count} product(s)")
   
   # Delete all banners
   banners_count = Banner.objects.count()
   Banner.objects.all().delete()
   print(f"✅ Deleted {banners_count} banner(s)")
   
   print("\n🎉 All products and banners have been deleted!")
   ```
4. Type `exit()` to exit the shell

### Option B: Using Script File

1. The file `delete_all_data.py` is already created in the backend directory
2. Run:
   ```bash
   python manage.py shell < delete_all_data.py
   ```

## Method 2: Using Django Admin Interface

1. Go to your Django admin URL: `https://your-backend-url.com/edith-admin-login/`
2. Login with admin credentials
3. Navigate to **Shop** section
4. Click on **Products**
5. Select all products (check the box at the top to select all)
6. From the "Action" dropdown, select "Delete selected products"
7. Click "Go" and confirm
8. Repeat for **Banners**:
   - Click on **Banners**
   - Select all banners
   - Delete them

## Method 3: Using Python Script (Standalone)

Create a file `delete_data.py` in the backend directory:

```python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edithclothes.settings')
django.setup()

from shop.models import Product, Banner

# Delete all products
products_count = Product.objects.count()
Product.objects.all().delete()
print(f"✅ Deleted {products_count} product(s)")

# Delete all banners
banners_count = Banner.objects.count()
Banner.objects.all().delete()
print(f"✅ Deleted {banners_count} banner(s)")

print("\n🎉 All products and banners have been deleted!")
```

Then run:
```bash
python delete_data.py
```

## Method 4: Using Management Command (Advanced)

If you want to create a reusable management command:

1. Create directory: `backend/shop/management/commands/`
2. Create file: `delete_all_products_banners.py`
3. Add the command code (see below)
4. Run: `python manage.py delete_all_products_banners`

## Quick One-Liner (Django Shell)

```bash
python manage.py shell -c "from shop.models import Product, Banner; print(f'Deleted {Product.objects.count()} products'); Product.objects.all().delete(); print(f'Deleted {Banner.objects.count()} banners'); Banner.objects.all().delete()"
```

## Important Notes

⚠️ **WARNING**: These operations are **PERMANENT** and **CANNOT BE UNDONE**!

- Deleting products will also delete:
  - All product variants
  - All product images
  - All cart items referencing those products
  - All order items referencing those products (orders themselves remain)

- Deleting banners will only delete the banner records and their associated media files

## Verify Deletion

After deletion, verify:
```python
from shop.models import Product, Banner
print(f"Products remaining: {Product.objects.count()}")
print(f"Banners remaining: {Banner.objects.count()}")
```

