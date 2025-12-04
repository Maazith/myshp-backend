# 🔐 Admin Login Fix

## ✅ What I've Done:

1. **Created `ensure_admin_user` command** - Guarantees an admin user exists
2. **Updated startup script** - Automatically creates/resets admin on deployment
3. **Default credentials** - Admin user will be created with default credentials

## 🔑 Default Admin Credentials:

After deployment, the admin user will be created with:

- **Username:** `admin`
- **Email:** `admin@example.com`
- **Password:** `admin123`

## 🔧 How to Change Credentials:

### Option 1: Environment Variables (Recommended)

Set these in Render Dashboard → myshp-backend → Environment:

```
DJANGO_SUPERUSER_USERNAME=your_username
DJANGO_SUPERUSER_EMAIL=your_email@example.com
DJANGO_SUPERUSER_PASSWORD=your_secure_password
```

### Option 2: Reset Password via Shell

1. Go to Render Dashboard → myshp-backend → Shell
2. Run:
```bash
python manage.py ensure_admin_user --username admin --password YourNewPassword123 --reset
```

## 🚀 After Deployment:

1. **Wait 2-3 minutes** for Render to deploy
2. **Go to:** `https://myshp-backend.onrender.com/admin/login/`
3. **Login with:**
   - Username: `admin`
   - Password: `admin123` (or your custom password)

## ⚠️ Security Note:

**Change the default password immediately after first login!**

The default password (`admin123`) is not secure for production.

## 🔍 Troubleshooting:

### If login still fails:

1. **Check Render Logs:**
   - Go to Render Dashboard → myshp-backend → Logs
   - Look for "Created new superuser" or "Reset password" messages

2. **Verify user exists:**
   ```bash
   # In Render Shell
   python manage.py shell
   ```
   ```python
   from django.contrib.auth.models import User
   User.objects.filter(is_superuser=True).values('username', 'email', 'is_active')
   ```

3. **Manually create user:**
   ```bash
   # In Render Shell
   python manage.py ensure_admin_user --username admin --password admin123 --reset
   ```

## 📋 What Happens on Each Deployment:

1. Migrations run automatically
2. Admin user is created/reset automatically
3. Server starts with Gunicorn

**You should always be able to login after deployment!**

