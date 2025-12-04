# 🔐 Admin Login Troubleshooting Guide

## Problem: "Login is invalid" or "Invalid username or password"

### ✅ Step 1: Verify Admin User Exists

**Option A: Using Render Shell (Starter plan and above)**
1. Go to Render Dashboard → **myshp-backend** → **Shell** → **Connect**
2. Run:
   ```bash
   python manage.py shell
   ```
3. In Python shell:
   ```python
   from django.contrib.auth.models import User
   
   # List all users
   users = User.objects.all()
   for u in users:
       print(f"Username: {u.username}, Email: {u.email}, is_staff: {u.is_staff}, is_superuser: {u.is_superuser}")
   
   # Check specific user
   try:
       user = User.objects.get(username='admin')  # Replace 'admin' with your username
       print(f"User found: {user.username}")
       print(f"is_staff: {user.is_staff}")
       print(f"is_superuser: {user.is_superuser}")
   except User.DoesNotExist:
       print("User not found!")
   ```

**Option B: Using Environment Variables (Recommended)**
1. Go to Render Dashboard → **myshp-backend** → **Environment**
2. Add these environment variables:
   ```
   DJANGO_SUPERUSER_USERNAME = admin
   DJANGO_SUPERUSER_EMAIL = your-email@gmail.com
   DJANGO_SUPERUSER_PASSWORD = YourStrongPassword123!
   ```
3. Save and redeploy
4. The superuser will be created automatically on startup

---

### ✅ Step 2: Create Admin User Manually

**If no admin user exists:**

**Using Render Shell:**
```bash
python manage.py createsuperuser
```
Follow prompts:
- Username: `admin` (or your choice)
- Email: `your-email@gmail.com`
- Password: Enter a strong password

**Or using Python shell:**
```python
from django.contrib.auth.models import User

# Create superuser
User.objects.create_superuser(
    username='admin',
    email='your-email@gmail.com',
    password='YourStrongPassword123!'
)

# Verify
user = User.objects.get(username='admin')
print(f"Created: {user.username}, is_staff: {user.is_staff}, is_superuser: {user.is_superuser}")
```

---

### ✅ Step 3: Make Existing User Admin

**If user exists but isn't admin:**

```python
from django.contrib.auth.models import User

user = User.objects.get(username='your-username')
user.is_staff = True
user.is_superuser = True
user.save()

print(f"User {user.username} is now admin!")
```

---

### ✅ Step 4: Reset Password

**If you forgot the password:**

```python
from django.contrib.auth.models import User

user = User.objects.get(username='admin')
user.set_password('NewPassword123!')
user.save()

print(f"Password reset for {user.username}")
```

---

### ✅ Step 5: Test Login

1. Go to: `https://myshp-frontend.vercel.app/admin/login.html`
2. Enter:
   - Username: `admin` (or your username)
   - Password: Your password
3. Click **Login**

---

## Common Issues

### Issue 1: "Invalid username or password"
**Solution:**
- Verify username is correct (case-sensitive)
- Verify password is correct
- Check if user exists in database (Step 1)
- Reset password if needed (Step 4)

### Issue 2: "Not authorized as admin"
**Solution:**
- User exists but `is_staff=False`
- Make user admin (Step 3)

### Issue 3: "Cannot connect to server"
**Solution:**
- Check if backend is running: `https://myshp-backend.onrender.com/api/`
- Verify API_BASE URL in `frontend/assets/js/api.js` is correct
- Check Render deployment status

### Issue 4: User doesn't exist
**Solution:**
- Create admin user (Step 2)
- Or use environment variables for auto-creation

---

## Quick Fix Commands

**Create admin user quickly:**
```bash
python manage.py shell
```
Then:
```python
from django.contrib.auth.models import User
User.objects.create_superuser('admin', 'admin@example.com', 'YourPassword123!')
```

**Make existing user admin:**
```python
from django.contrib.auth.models import User
u = User.objects.get(username='your-username')
u.is_staff = True
u.is_superuser = True
u.save()
```

**Reset password:**
```python
from django.contrib.auth.models import User
u = User.objects.get(username='admin')
u.set_password('NewPassword123!')
u.save()
```

---

## Verify Everything Works

1. ✅ Admin user exists
2. ✅ `is_staff = True`
3. ✅ `is_superuser = True`
4. ✅ Password is correct
5. ✅ Backend is running
6. ✅ Frontend API URL is correct

---

## Still Having Issues?

1. Check browser console (F12) for errors
2. Check Render logs for backend errors
3. Verify environment variables are set correctly
4. Try creating a fresh admin user
5. Clear browser cache and cookies

---

**Need Help?** Check the backend logs in Render dashboard for detailed error messages.

