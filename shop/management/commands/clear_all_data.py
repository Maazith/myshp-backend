"""
Management command to clear all demo/test data from the database
WARNING: This will delete all products, categories, banners, orders, carts, etc.
Only SiteSettings and Users are preserved.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import (
    Category,
    Product,
    ProductVariant,
    ProductImage,
    Banner,
    Cart,
    CartItem,
    Order,
    OrderItem,
    PaymentProof,
    SiteSettings,
)


class Command(BaseCommand):
    help = 'Clear all demo/test data (products, categories, banners, orders, carts). Preserves SiteSettings and Users.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Skip confirmation prompt',
        )

    def handle(self, *args, **options):
        if not options['force']:
            self.stdout.write(self.style.WARNING(
                '⚠️  WARNING: This will delete ALL:'
            ))
            self.stdout.write('   - Products and Variants')
            self.stdout.write('   - Categories')
            self.stdout.write('   - Banners')
            self.stdout.write('   - Orders and Order Items')
            self.stdout.write('   - Carts and Cart Items')
            self.stdout.write('   - Payment Proofs')
            self.stdout.write('')
            self.stdout.write('   PRESERVED:')
            self.stdout.write('   - Users')
            self.stdout.write('   - Site Settings')
            self.stdout.write('')
            confirm = input('Type "yes" to continue: ')
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.ERROR('Operation cancelled.'))
                return

        # Count before deletion
        product_count = Product.objects.count()
        category_count = Category.objects.count()
        banner_count = Banner.objects.count()
        order_count = Order.objects.count()
        cart_count = Cart.objects.count()

        # Delete in correct order (respecting foreign keys)
        self.stdout.write('🗑️  Deleting data...')
        
        # Delete orders and related data
        PaymentProof.objects.all().delete()
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'   ✓ Deleted {order_count} orders'))

        # Delete carts
        CartItem.objects.all().delete()
        Cart.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'   ✓ Deleted {cart_count} carts'))

        # Delete products and related data
        ProductImage.objects.all().delete()
        ProductVariant.objects.all().delete()
        Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'   ✓ Deleted {product_count} products'))

        # Delete categories
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'   ✓ Deleted {category_count} categories'))

        # Delete banners
        Banner.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'   ✓ Deleted {banner_count} banners'))

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('✅ All demo data cleared successfully!'))
        self.stdout.write('')
        self.stdout.write('📝 Next steps:')
        self.stdout.write('   1. Create categories: python manage.py create_demo_data')
        self.stdout.write('   2. Or add data manually via Admin panel')
        self.stdout.write('   3. Update Site Settings: python manage.py update_contact_info')

