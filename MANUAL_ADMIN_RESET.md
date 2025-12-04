# 🔧 Manual Admin Password Reset

## ⚠️ If Login Still Fails After Setting Environment Variables

The environment variables might not have been picked up, or the user might need to be manually reset.

## 🔍 Step 1: Verify Environment Variables

1. Go to **Render Dashboard** → **myshp-backend** → **Environment**
2. Verify these are set:
   - `DJANGO_SUPERUSER_USERNAME` (e.g., `admin`)
   - `DJANGO_SUPERUSER_EMAIL` (e.g., `admin@example.com`)
   - `DJANGO_SUPERUSER_PASSWORD` (your password)

3. **Important:** After setting environment variables, you need to **redeploy** the service for them to take effect!

## 🔄 Step 2: Manual Reset via Render Shell

1. Go to **Render Dashboard** → **myshp-backend** → **Shell**
2. Run this command (replace with your actual credentials):

```bash
python manage.py ensure_admin_user --username admin --email admin@example.com --password YourPassword123 --reset
```

**Example:**
```bash
python manage.py ensure_admin_user --username admin --email admin@example.com --password MySecurePass123 --reset
```

3. You should see:
```
✅ Reset password and updated superuser: admin
```

## 🔑 Step 3: Try Login Again

1. Go to: `https://myshp-backend.onrender.com/admin/login/`
2. Use the credentials you just set

## 🐛 Troubleshooting

### If Shell is Not Available:

If Render Shell requires upgrade, you can:

1. **Redeploy the service** - This will trigger the startup script which runs `ensure_admin_user --reset`
2. **Check Render Logs** - Look for "Ensuring admin user exists" and "Reset password" messages

### If Environment Variables Aren't Working:

1. **Double-check spelling:**
   - `DJANGO_SUPERUSER_USERNAME` (not `DJANGO_SUPERUSER_NAME`)
   - `DJANGO_SUPERUSER_EMAIL` (not `DJANGO_SUPERUSER_MAIL`)
   - `DJANGO_SUPERUSER_PASSWORD` (not `DJANGO_SUPERUSER_PASS`)

2. **Redeploy after setting variables:**
   - Environment variables only take effect after redeployment
   - Go to Render Dashboard → myshp-backend → **Manual Deploy** → **Deploy latest commit**

3. **Check logs for what credentials were used:**
   - Look for: `📋 Using credentials:`
   - Verify username and email match what you set

### Verify User Exists:

In Render Shell, run:
```bash
python manage.py shell
```

Then:
```python
from django.contrib.auth.models import User
users = User.objects.filter(is_superuser=True)
for u in users:
    print(f"Username: {u.username}, Email: {u.email}, Active: {u.is_active}, Staff: {u.is_staff}, Superuser: {u.is_superuser}")
```

### Test Password:

In Django shell:
```python
from django.contrib.auth.models import User
user = User.objects.get(username='admin')
user.check_password('YourPassword123')  # Should return True
```

## ✅ Success Indicators

After running `ensure_admin_user --reset`, you should see:
- ✅ Reset password and updated superuser: [username]
- Admin Login Credentials displayed

Then login should work!

---

**Most Common Issue:** Environment variables are set but service wasn't redeployed. **Redeploy the service** after setting environment variables!

