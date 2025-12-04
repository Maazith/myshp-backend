"""
Management command to create superuser from environment variables.
Usage: python manage.py create_superuser_from_env
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates a superuser from environment variables'

    def handle(self, *args, **options):
        admin_username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        admin_email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        admin_password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not all([admin_username, admin_email, admin_password]):
            self.stdout.write(
                self.style.WARNING(
                    'Superuser not created. Set these environment variables:\n'
                    'DJANGO_SUPERUSER_USERNAME\n'
                    'DJANGO_SUPERUSER_EMAIL\n'
                    'DJANGO_SUPERUSER_PASSWORD'
                )
            )
            return

        if User.objects.filter(username=admin_username).exists():
            self.stdout.write(
                self.style.SUCCESS(f'Superuser "{admin_username}" already exists.')
            )
            return

        User.objects.create_superuser(
            username=admin_username,
            email=admin_email,
            password=admin_password
        )
        self.stdout.write(
            self.style.SUCCESS(f'Superuser "{admin_username}" created successfully!')
        )

