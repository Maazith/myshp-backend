# 🔐 Create Admin User / Superuser

## Problem: Cannot Login as Admin

If you cannot login to the Django admin panel, you need to create a superuser account.

---

## ✅ Solution 1: Automatic Creation (Recommended)

### Using Environment Variables on Render

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Click on **"myshp-backend"** service

2. **Go to Environment Variables**
   - Click **"Environment"** in the left sidebar
   - Or go to **"Settings"** → **"Environment Variables"**

3. **Add These Environment Variables:**
   ```
   DJANGO_SUPERUSER_USERNAME = admin
   DJANGO_SUPERUSER_EMAIL = your-email@gmail.com
   DJANGO_SUPERUSER_PASSWORD = your-strong-password-here
   ```
   
   **Important:** Use a strong password (at least 8 characters, mix of letters, numbers, symbols)

4. **Save and Redeploy**
   - Click **"Save Changes"**
   - Go to **"Manual Deploy"** → **"Deploy latest commit"**

5. **After Deployment**
   - The superuser will be created automatically on startup
   - Login at: `https://myshp-backend.onrender.com/admin/`

---

## ✅ Solution 2: Manual Creation via Render Shell

### If you have Shell access (Starter plan and above):

1. **Open Render Shell**
   - Go to Render Dashboard → **"myshp-backend"** → **"Shell"**
   - Click **"Connect"** to open shell

2. **Run Migration (if needed)**
   ```bash
   python manage.py migrate
   ```

3. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```
   
   Follow the prompts:
   - Username: `admin` (or your choice)
   - Email: `your-email@gmail.com`
   - Password: Enter a strong password (twice)

4. **Login**
   - Go to: `https://myshp-backend.onrender.com/admin/`
   - Use the username and password you just created

---

## ✅ Solution 3: Using Management Command

### If you have Shell access:

```bash
# Set environment variables first
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_EMAIL=your-email@gmail.com
export DJANGO_SUPERUSER_PASSWORD=your-password

# Run the command
python manage.py create_superuser_from_env
```

---

## 🔍 Troubleshooting

### "Please enter the correct username and password"
- **Check:** Username and password are correct
- **Check:** User exists in database (migrations ran)
- **Check:** User has `is_staff=True` and `is_superuser=True`

### "No such user"
- **Solution:** Create superuser using one of the methods above

### "This account is inactive"
- **Solution:** User account might be inactive
- **Fix:** Use Shell to activate: `python manage.py shell` then:
  ```python
  from django.contrib.auth import get_user_model
  User = get_user_model()
  user = User.objects.get(username='admin')
  user.is_active = True
  user.is_staff = True
  user.is_superuser = True
  user.save()
  ```

### Cannot access Shell (Free plan)
- **Solution:** Use Solution 1 (Environment Variables)
- The `start.sh` script will automatically create superuser on startup

---

## 📝 Admin URLs

- **Django Admin:** `https://myshp-backend.onrender.com/admin/`
- **Admin Dashboard:** `https://myshp-backend.onrender.com/admin/dashboard/`

---

## 🔒 Security Notes

- Use a **strong password** (at least 12 characters recommended)
- Don't share admin credentials
- Consider using environment variables instead of hardcoding
- Change password regularly

---

## ✅ Quick Setup

**Fastest way:** Add environment variables in Render dashboard:
1. `DJANGO_SUPERUSER_USERNAME` = `admin`
2. `DJANGO_SUPERUSER_EMAIL` = `your-email@gmail.com`
3. `DJANGO_SUPERUSER_PASSWORD` = `your-strong-password`

Then redeploy. The superuser will be created automatically!

