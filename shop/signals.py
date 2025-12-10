from django.db.models.signals import post_migrate
from django.contrib.auth.models import User
from django.dispatch import receiver


@receiver(post_migrate)
def create_default_superuser(sender, **kwargs):
    """Auto-create superuser after migrations"""
    username = 'Edithcloths'
    email = 'edith0530s@gmail.com'
    password = 'edithcloths0530@2025./'
    
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"[OK] Created superuser: {username}")
    else:
        # Update existing superuser password if username matches
        user = User.objects.filter(username=username).first()
        if user and user.is_superuser:
            user.set_password(password)
            user.email = email
            user.save()
            print(f"[OK] Updated superuser password: {username}")

