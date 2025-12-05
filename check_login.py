"""
Quick script to check and fix login issues
Run: python manage.py shell < check_login.py
Or: python check_login.py (after setting Django settings)
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edithclothes.settings')
django.setup()

from django.contrib.auth.models import User

username = 'Maazith'
email = 'maazith.md@gmail.com'
password = 'maazith2005'

print("=" * 50)
print("CHECKING LOGIN SETUP")
print("=" * 50)
print()

# Check if user exists
user = User.objects.filter(username=username).first()

if user:
    print(f"✓ User '{username}' EXISTS")
    print(f"  Email: {user.email}")
    print(f"  Is staff: {user.is_staff}")
    print(f"  Is superuser: {user.is_superuser}")
    
    # Check password
    if user.check_password(password):
        print(f"  ✓ Password is CORRECT")
    else:
        print(f"  ✗ Password is WRONG - resetting...")
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print(f"  ✓ Password reset to '{password}'")
        print(f"  ✓ Staff and superuser privileges set")
else:
    print(f"✗ User '{username}' does NOT exist")
    print(f"Creating superuser...")
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f"✓ Superuser created successfully!")
    print(f"  Username: {username}")
    print(f"  Email: {email}")
    print(f"  Password: {password}")

print()
print("=" * 50)
print("You can now login with:")
print(f"  Username: {username}")
print(f"  Password: {password}")
print("=" * 50)




