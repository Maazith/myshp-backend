from django.db.models.signals import post_migrate
from django.contrib.auth.models import User
from django.dispatch import receiver


@receiver(post_migrate)
def create_default_superuser(sender, **kwargs):
    """Auto-create superuser after migrations"""
    username = 'Maazith'
    email = 'maazith.md@gmail.com'
    password = 'maazith2005'
    
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✓ Created superuser: {username}")

