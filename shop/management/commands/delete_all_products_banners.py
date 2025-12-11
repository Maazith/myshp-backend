"""
Django management command to delete all products and banners.
Usage: python manage.py delete_all_products_banners
"""

import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from shop.models import Product, Banner


class Command(BaseCommand):
    help = 'Delete all products and banners from the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--products-only',
            action='store_true',
            help='Delete only products',
        )
        parser.add_argument(
            '--banners-only',
            action='store_true',
            help='Delete only banners',
        )
        parser.add_argument(
            '--no-input',
            action='store_true',
            help='Skip confirmation prompt',
        )
        parser.add_argument(
            '--delete-images',
            action='store_true',
            help='Also delete all product and banner image files from media directory',
        )

    def handle(self, *args, **options):
        delete_products = not options['banners_only']
        delete_banners = not options['products_only']
        
        if not options['no_input']:
            if delete_products and delete_banners:
                confirm = input(
                    '⚠️  WARNING: This will delete ALL products and banners. '
                    'This action cannot be undone!\n'
                    'Type "yes" to continue: '
                )
            elif delete_products:
                confirm = input(
                    '⚠️  WARNING: This will delete ALL products. '
                    'This action cannot be undone!\n'
                    'Type "yes" to continue: '
                )
            else:
                confirm = input(
                    '⚠️  WARNING: This will delete ALL banners. '
                    'This action cannot be undone!\n'
                    'Type "yes" to continue: '
                )
            
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.ERROR('Operation cancelled.'))
                return
        
        if delete_products:
            products_count = Product.objects.count()
            if products_count > 0:
                Product.objects.all().delete()
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Successfully deleted {products_count} product(s)')
                )
            else:
                self.stdout.write(self.style.WARNING('No products to delete.'))
        
        if delete_banners:
            banners_count = Banner.objects.count()
            if banners_count > 0:
                Banner.objects.all().delete()
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully deleted {banners_count} banner(s)')
                )
            else:
                self.stdout.write(self.style.WARNING('No banners to delete.'))
        
        # Delete media files if requested
        if options['delete_images']:
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
            
            if deleted_files > 0 or deleted_dirs > 0:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Deleted {deleted_files} image file(s) and {deleted_dirs} directory/directories from media folder'
                    )
                )
            else:
                self.stdout.write(self.style.WARNING('No image files to delete.'))
        
        self.stdout.write(self.style.SUCCESS('\nOperation completed!'))

