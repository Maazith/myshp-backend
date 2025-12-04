# 🔄 Running Migrations on Free Plan (Without Shell)

Since Shell is not available on Free plan, here are alternative methods:

---

## ✅ Method 1: Automatic Migrations (Recommended)

**Already configured!** The `start.sh` script automatically runs migrations on every startup.

### How it works:
- Migrations run automatically when the service starts
- No manual intervention needed
- Safe to run multiple times (idempotent)

### What happens:
1. Service starts → `start.sh` runs
2. Migrations execute automatically
3. Gunicorn starts

**You don't need to do anything!** Migrations will run automatically.

---

## ✅ Method 2: Create Superuser via Environment Variables

### Step 1: Add Environment Variables in Render

Go to your service → **Environment** tab → Add these variables:

```
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=your-email@gmail.com
DJANGO_SUPERUSER_PASSWORD=your-strong-password
```

### Step 2: Update Build Command (One-time)

1. Go to **Settings** → **Build & Deploy**
2. Update **Build Command** to:
   ```bash
   pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py create_superuser_from_env
   ```
3. Click **"Save Changes"**
4. Render will redeploy automatically

### Step 3: Remove from Build Command (After First Deploy)

Once superuser is created, remove the command from build:
1. Go to **Settings** → **Build & Deploy**
2. Update **Build Command** back to:
   ```bash
   pip install -r requirements.txt && python manage.py collectstatic --noinput
   ```
3. Save changes

---

## ✅ Method 3: Manual Deploy with Command

1. Go to your service → **Manual Deploy** dropdown
2. Select **"Deploy latest commit"**
3. Before deploying, you can add a one-time command in **Settings** → **Build Command**:
   ```bash
   pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py create_superuser_from_env
   ```
4. Deploy, then remove the extra commands

---

## ✅ Method 4: Use Django Admin API (After Migrations)

Once migrations are done (automatic), you can create superuser via API:

### Option A: Register via API
1. Use your registration endpoint:
   ```
   POST https://myshp-backend.onrender.com/api/auth/register
   ```
   Body:
   ```json
   {
     "username": "admin",
     "email": "your-email@gmail.com",
     "password": "your-password"
   }
   ```

2. Then manually make user staff/superuser via database (if you have access)

### Option B: Use Django Admin Panel
- If you can access admin panel, you might be able to create users there

---

## 🎯 Recommended Approach

**For Migrations:**
- ✅ Already automatic via `start.sh` - no action needed!

**For Superuser:**
- ✅ Use **Method 2** (Environment Variables) - easiest and most secure

---

## 📝 Quick Steps Summary

1. **Migrations**: Already automatic ✅
2. **Superuser**: 
   - Add environment variables: `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD`
   - Update build command temporarily to include `python manage.py create_superuser_from_env`
   - Deploy
   - Remove from build command

---

## 🔍 Verify Migrations Ran

Check your service logs:
1. Go to **Logs** tab
2. Look for: `🔄 Running database migrations...`
3. Should see: `✅ Migrations complete!`

---

## 🐛 Troubleshooting

### Migrations Not Running:
- Check `start.sh` exists in your repository
- Verify start command is: `bash start.sh`
- Check logs for errors

### Superuser Not Created:
- Verify environment variables are set correctly
- Check logs for errors
- Try Method 3 (Manual Deploy)

---

**Migrations run automatically! Just create superuser using environment variables.** 🚀

