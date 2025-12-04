"""
Management command to update SiteSettings contact information
"""
from django.core.management.base import BaseCommand
from shop.models import SiteSettings


class Command(BaseCommand):
    help = 'Update SiteSettings contact information (phone, email, address)'

    def handle(self, *args, **options):
        # Get or create SiteSettings instance
        settings = SiteSettings.load()
        
        # Update contact information
        settings.contact_phone = '6381902506'
        settings.contact_email = 'edith0530s@gmail.com'
        settings.contact_address = '35/1 sivan sannadhi street keeranur (PT) kulathur (TK) Pudukkottai (DT) 622502'
        settings.whatsapp_number = '6381902506'  # Also update WhatsApp number
        
        settings.save()
        
        self.stdout.write(
            self.style.SUCCESS('✅ Successfully updated contact information:')
        )
        self.stdout.write(f'   Phone: {settings.contact_phone}')
        self.stdout.write(f'   Email: {settings.contact_email}')
        self.stdout.write(f'   Address: {settings.contact_address}')
        self.stdout.write(f'   WhatsApp: {settings.whatsapp_number}')

