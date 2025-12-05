"""
Django management command to delete all products and banners.
Usage: python manage.py delete_all_products_banners
"""

from django.core.management.base import BaseCommand
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
                    self.style.SUCCESS(f'✅ Successfully deleted {banners_count} banner(s)')
                )
            else:
                self.stdout.write(self.style.WARNING('No banners to delete.'))
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Operation completed!'))

