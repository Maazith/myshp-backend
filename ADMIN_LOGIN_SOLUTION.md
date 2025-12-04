# 🔐 Admin Login Solution - Environment Variables Not Working

## ⚠️ Problem

You set environment variables but still getting "invalid username or password".

## ✅ Solution

### Step 1: Verify Environment Variables Are Set Correctly

1. Go to **Render Dashboard** → **myshp-backend** → **Environment**
2. Make sure these are set **exactly** (case-sensitive):
   - `DJANGO_SUPERUSER_USERNAME` = your username (e.g., `admin`)
   - `DJANGO_SUPERUSER_EMAIL` = your email (e.g., `admin@example.com`)
   - `DJANGO_SUPERUSER_PASSWORD` = your password (e.g., `MyPassword123`)

### Step 2: REDEPLOY THE SERVICE (CRITICAL!)

**Environment variables only take effect after redeployment!**

1. Go to **Render Dashboard** → **myshp-backend**
2. Click **"Manual Deploy"** → **"Deploy latest commit"**
3. Wait 2-3 minutes for deployment to complete

### Step 3: Check Logs

After deployment, check **Render Logs** for:
```
👤 Ensuring admin user exists...
📋 Checking environment variables...
  DJANGO_SUPERUSER_USERNAME: [your username]
  DJANGO_SUPERUSER_EMAIL: [your email]
  DJANGO_SUPERUSER_PASSWORD: set (hidden)
📋 Using credentials:
   Username: [your username]
   Email: [your email]
   Password: ******** (hidden)
✅ Reset password and updated superuser: [username]
```

### Step 4: Try Login

1. Go to: `https://myshp-backend.onrender.com/admin/login/`
2. Use the **exact** username and password from your environment variables

---

## 🔧 Alternative: Manual Reset via Shell

If redeployment doesn't work, manually reset via Render Shell:

1. Go to **Render Dashboard** → **myshp-backend** → **Shell**
2. Run:
```bash
python manage.py ensure_admin_user --username YOUR_USERNAME --email YOUR_EMAIL --password YOUR_PASSWORD --reset
```

**Example:**
```bash
python manage.py ensure_admin_user --username admin --email admin@example.com --password MySecurePass123 --reset
```

3. You should see:
```
✅ Reset password and updated superuser: admin
```

4. Try login again

---

## 🐛 Common Issues

### Issue 1: Environment Variables Set But Not Applied
**Solution:** You MUST redeploy after setting environment variables!

### Issue 2: Wrong Variable Names
**Check spelling:**
- ✅ `DJANGO_SUPERUSER_USERNAME` (correct)
- ❌ `DJANGO_SUPERUSER_NAME` (wrong)
- ❌ `DJANGO_ADMIN_USERNAME` (wrong)

### Issue 3: Password Has Special Characters
**Solution:** If password has special characters, wrap it in quotes in Shell:
```bash
python manage.py ensure_admin_user --username admin --password "My@Pass#123" --reset
```

### Issue 4: User Exists But Password Wrong
**Solution:** The updated code now **always resets the password** on startup, so redeploy and it should work.

---

## ✅ What Changed

The code now **always resets the admin password** when the service starts, ensuring:
- Environment variables always take effect
- Password always matches what you set
- No need to manually reset

**Just redeploy after setting environment variables!**

---

## 📋 Quick Checklist

- [ ] Environment variables set correctly in Render Dashboard
- [ ] Service redeployed after setting variables
- [ ] Checked logs to verify credentials were used
- [ ] Tried login with exact username/password from env vars
- [ ] If still fails, manually reset via Shell

---

**Most Common Fix:** **Redeploy the service** after setting environment variables!

