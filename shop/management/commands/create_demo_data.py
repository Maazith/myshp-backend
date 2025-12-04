from django.core.management.base import BaseCommand
from shop.models import Category, Product, ProductVariant, Banner, SiteSettings
from decimal import Decimal


class Command(BaseCommand):
    help = 'Create demo data for the website'

    def handle(self, *args, **options):
        self.stdout.write('Creating demo data...')

        # Create SiteSettings if not exists
        settings = SiteSettings.load()
        if not settings.logo:
            settings.website_name = 'EdithCloths'
            settings.upi_id = 'your-upi-id@paytm'
            settings.contact_phone = '6381902506'
            settings.contact_email = 'edith0530s@gmail.com'
            settings.contact_address = '35/1 sivan sannadhi street keeranur (PT) kulathur (TK) Pudukkottai (DT) 622502'
            settings.whatsapp_number = '6381902506'
            settings.about_text = 'EdithCloths is your premium destination for luxury fashion. We offer the finest quality clothing for men and women.'
            settings.save()
            self.stdout.write(self.style.SUCCESS('✓ Created SiteSettings'))

        # Create Categories
        categories_data = [
            {'name': 'T-Shirts', 'description': 'Premium quality t-shirts'},
            {'name': 'Shirts', 'description': 'Classic and modern shirts'},
            {'name': 'Dresses', 'description': 'Elegant dresses for every occasion'},
            {'name': 'Jeans', 'description': 'Comfortable and stylish jeans'},
        ]
        
        categories = []
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories.append(cat)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created category: {cat.name}'))

        # Create Products
        products_data = [
            {
                'title': 'Premium Cotton T-Shirt',
                'description': 'Comfortable and stylish premium cotton t-shirt. Perfect for casual wear.',
                'base_price': Decimal('1299.00'),
                'gender': 'MEN',
                'category': categories[0],
                'variants': [
                    {'size': 'S', 'color': 'Black', 'stock': 10},
                    {'size': 'M', 'color': 'Black', 'stock': 15},
                    {'size': 'L', 'color': 'Black', 'stock': 12},
                    {'size': 'XL', 'color': 'Black', 'stock': 8},
                    {'size': 'M', 'color': 'White', 'stock': 20},
                    {'size': 'L', 'color': 'White', 'stock': 18},
                ]
            },
            {
                'title': 'Classic Formal Shirt',
                'description': 'Elegant formal shirt for office wear. Premium fabric with excellent fit.',
                'base_price': Decimal('2499.00'),
                'gender': 'MEN',
                'category': categories[1],
                'variants': [
                    {'size': 'S', 'color': 'White', 'stock': 8},
                    {'size': 'M', 'color': 'White', 'stock': 12},
                    {'size': 'L', 'color': 'White', 'stock': 10},
                    {'size': 'XL', 'color': 'White', 'stock': 5},
                    {'size': 'M', 'color': 'Blue', 'stock': 15},
                    {'size': 'L', 'color': 'Blue', 'stock': 13},
                ]
            },
            {
                'title': 'Summer Casual T-Shirt',
                'description': 'Lightweight and breathable t-shirt perfect for summer.',
                'base_price': Decimal('899.00'),
                'gender': 'UNISEX',
                'category': categories[0],
                'variants': [
                    {'size': 'S', 'color': 'Navy', 'stock': 20},
                    {'size': 'M', 'color': 'Navy', 'stock': 25},
                    {'size': 'L', 'color': 'Navy', 'stock': 22},
                    {'size': 'S', 'color': 'Grey', 'stock': 18},
                    {'size': 'M', 'color': 'Grey', 'stock': 20},
                ]
            },
            {
                'title': 'Elegant Evening Dress',
                'description': 'Stunning evening dress for special occasions. Made with premium fabric.',
                'base_price': Decimal('5999.00'),
                'gender': 'WOMEN',
                'category': categories[2],
                'variants': [
                    {'size': 'S', 'color': 'Black', 'stock': 5},
                    {'size': 'M', 'color': 'Black', 'stock': 8},
                    {'size': 'L', 'color': 'Black', 'stock': 6},
                    {'size': 'M', 'color': 'Red', 'stock': 4},
                    {'size': 'L', 'color': 'Red', 'stock': 3},
                ]
            },
            {
                'title': 'Slim Fit Jeans',
                'description': 'Modern slim fit jeans with excellent comfort and style.',
                'base_price': Decimal('2999.00'),
                'gender': 'MEN',
                'category': categories[3],
                'variants': [
                    {'size': 'S', 'color': 'Blue', 'stock': 10},
                    {'size': 'M', 'color': 'Blue', 'stock': 15},
                    {'size': 'L', 'color': 'Blue', 'stock': 12},
                    {'size': 'XL', 'color': 'Blue', 'stock': 8},
                ]
            },
            {
                'title': 'Floral Summer Dress',
                'description': 'Beautiful floral print dress perfect for summer days.',
                'base_price': Decimal('3499.00'),
                'gender': 'WOMEN',
                'category': categories[2],
                'variants': [
                    {'size': 'S', 'color': 'Floral', 'stock': 8},
                    {'size': 'M', 'color': 'Floral', 'stock': 10},
                    {'size': 'L', 'color': 'Floral', 'stock': 9},
                ]
            },
            {
                'title': 'Denim Jacket',
                'description': 'Classic denim jacket for casual styling.',
                'base_price': Decimal('3999.00'),
                'gender': 'UNISEX',
                'category': categories[3],
                'variants': [
                    {'size': 'M', 'color': 'Blue', 'stock': 7},
                    {'size': 'L', 'color': 'Blue', 'stock': 8},
                    {'size': 'XL', 'color': 'Blue', 'stock': 5},
                ]
            },
            {
                'title': 'Business Casual Shirt',
                'description': 'Perfect shirt for business casual occasions.',
                'base_price': Decimal('2199.00'),
                'gender': 'MEN',
                'category': categories[1],
                'variants': [
                    {'size': 'S', 'color': 'Grey', 'stock': 6},
                    {'size': 'M', 'color': 'Grey', 'stock': 10},
                    {'size': 'L', 'color': 'Grey', 'stock': 8},
                    {'size': 'M', 'color': 'Beige', 'stock': 9},
                    {'size': 'L', 'color': 'Beige', 'stock': 7},
                ]
            },
            {
                'title': 'Casual Maxi Dress',
                'description': 'Comfortable and stylish maxi dress for everyday wear.',
                'base_price': Decimal('2799.00'),
                'gender': 'WOMEN',
                'category': categories[2],
                'variants': [
                    {'size': 'S', 'color': 'Pink', 'stock': 5},
                    {'size': 'M', 'color': 'Pink', 'stock': 8},
                    {'size': 'L', 'color': 'Pink', 'stock': 6},
                ]
            },
            {
                'title': 'Skinny Fit Jeans',
                'description': 'Trendy skinny fit jeans with stretch fabric.',
                'base_price': Decimal('3199.00'),
                'gender': 'WOMEN',
                'category': categories[3],
                'variants': [
                    {'size': 'S', 'color': 'Black', 'stock': 7},
                    {'size': 'M', 'color': 'Black', 'stock': 10},
                    {'size': 'L', 'color': 'Black', 'stock': 8},
                ]
            },
        ]

        for prod_data in products_data:
            category = prod_data.pop('category')
            variants_data = prod_data.pop('variants')
            
            # Include category in defaults
            defaults = {**prod_data, 'category': category}
            
            product, created = Product.objects.get_or_create(
                title=prod_data['title'],
                defaults=defaults
            )
            if not created:
                # Update existing product
                for key, value in prod_data.items():
                    setattr(product, key, value)
                product.category = category
                product.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Updated product: {product.title}'))
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created product: {product.title}'))

            # Create variants
            for variant_data in variants_data:
                ProductVariant.objects.get_or_create(
                    product=product,
                    size=variant_data['size'],
                    color=variant_data['color'],
                    defaults={'stock': variant_data['stock']}
                )

        # Create Banners (they will be created but without images - admin can add images later)
        banners_data = [
            {'title': 'Summer Collection', 'subtitle': 'New Arrivals', 'display_order': 1},
            {'title': 'Premium Quality', 'subtitle': 'Luxury Fashion', 'display_order': 2},
            {'title': 'Special Offers', 'subtitle': 'Limited Time', 'display_order': 3},
        ]

        for banner_data in banners_data:
            Banner.objects.get_or_create(
                title=banner_data['title'],
                defaults={
                    'subtitle': banner_data['subtitle'],
                    'display_order': banner_data['display_order'],
                    'is_active': True
                }
            )

        self.stdout.write(self.style.SUCCESS('✓ Demo data created successfully!'))

