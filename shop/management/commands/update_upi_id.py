"""
Management command to update SiteSettings UPI ID
"""
from django.core.management.base import BaseCommand
from shop.models import SiteSettings


class Command(BaseCommand):
    help = 'Update SiteSettings UPI ID for payment processing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--upi-id',
            type=str,
            required=True,
            help='UPI ID to set (e.g., maazith.md@oksbi)',
        )

    def handle(self, *args, **options):
        upi_id = options['upi_id']
        
        # Get or create SiteSettings instance
        settings = SiteSettings.load()
        
        # Update UPI ID
        settings.upi_id = upi_id
        settings.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Successfully updated UPI ID to: {upi_id}')
        )
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('UPI ID Updated:'))
        self.stdout.write(self.style.SUCCESS(f'  UPI ID: {upi_id}'))
        self.stdout.write(self.style.SUCCESS('='*50 + '\n'))
        
        self.stdout.write(
            self.style.WARNING('Note: You may need to update the QR code image in the admin panel.')
        )

