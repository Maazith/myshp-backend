"""
Management command to ensure an admin user exists.
Creates a superuser if one doesn't exist, or resets password if user exists.
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Ensure an admin user exists. Creates one if needed, or resets password if user exists.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default=None,
            help='Admin username (defaults to DJANGO_SUPERUSER_USERNAME or "admin")',
        )
        parser.add_argument(
            '--email',
            type=str,
            default=None,
            help='Admin email (defaults to DJANGO_SUPERUSER_EMAIL or "admin@example.com")',
        )
        parser.add_argument(
            '--password',
            type=str,
            default=None,
            help='Admin password (defaults to DJANGO_SUPERUSER_PASSWORD or "admin123")',
        )
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset password even if user exists',
        )

    def handle(self, *args, **options):
        # Get credentials from arguments, environment, or defaults
        # Priority: command args > environment variables > defaults
        username = (
            options['username']
            or os.environ.get('DJANGO_SUPERUSER_USERNAME')
            or 'Edithcloths'
        )
        email = (
            options['email']
            or os.environ.get('DJANGO_SUPERUSER_EMAIL')
            or 'edith0530s@gmail.com'
        )
        password = (
            options['password']
            or os.environ.get('DJANGO_SUPERUSER_PASSWORD')
            or 'edithcloths0530@2025./'
        )
        
        # Log what we're using (hide password)
        self.stdout.write(f'📋 Using credentials:')
        self.stdout.write(f'   Username: {username}')
        self.stdout.write(f'   Email: {email}')
        self.stdout.write(f'   Password: {"*" * len(password)} (hidden)')

        # Check if user exists
        user_exists = User.objects.filter(username=username).exists()

        if user_exists:
            # Always reset password and ensure user is active and superuser
            # This ensures environment variables always take effect
            user = User.objects.get(username=username)
            user.set_password(password)
            user.email = email
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Reset password and updated superuser: {username}'
                )
            )
        else:
            # Create new superuser
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Created new superuser: {username}'
                )
            )

        # Display login info
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('Admin Login Credentials:'))
        self.stdout.write(self.style.SUCCESS(f'  Username: {username}'))
        self.stdout.write(self.style.SUCCESS(f'  Email: {email}'))
        self.stdout.write(self.style.SUCCESS(f'  Password: {password}'))
        self.stdout.write(self.style.SUCCESS('='*50 + '\n'))

