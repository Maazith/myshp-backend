# 🔍 Debugging 500 Error on Admin Login

## Current Status
- ✅ Deployments successful (commits 1e6f045, d05bbb7)
- ❌ Admin login still showing 500 error
- ⚠️ Need to check Render logs for actual error

## Steps to Debug

### 1. Check Render Logs
Go to Render Dashboard → myshp-backend → Logs

**Look for:**
- Python traceback errors
- Template errors
- Static file errors
- Database connection errors
- Import errors

### 2. Common Causes

#### A. Static Files Not Collected
**Symptom:** Template tries to load CSS/JS that doesn't exist

**Fix:**
```bash
# In Render Shell or build command
python manage.py collectstatic --noinput
```

#### B. Template Error
**Symptom:** Template syntax error or missing template

**Fix:** Check `backend/templates/registration/login.html` for syntax errors

#### C. Database Connection
**Symptom:** Database query fails

**Fix:** Check DATABASE_URL environment variable

#### D. Import Error
**Symptom:** Python import fails

**Fix:** Check all imports in `backend/shop/admin.py` and `backend/edithclothes/urls.py`

### 3. Quick Fixes Applied

1. **Simplified Static Files Storage:**
   - Added fallback for WhiteNoise storage
   - Prevents errors if manifest file doesn't exist

2. **Error Handling:**
   - Added try-except for media file serving
   - Added error handling for media directory creation

3. **Security Settings:**
   - Disabled SECURE_SSL_REDIRECT (Render handles HTTPS)
   - Fixed ALLOWED_HOSTS syntax

### 4. Next Steps

1. **Check Render Logs** - Most important!
2. **Verify Static Files Collected:**
   - Check if `staticfiles` directory exists
   - Check if `admin/css/custom_admin.css` exists in staticfiles

3. **Test Without Custom Template:**
   - Temporarily rename `backend/templates/registration/login.html`
   - See if default Django admin login works

4. **Check Database:**
   - Verify migrations ran successfully
   - Check if admin user exists

### 5. Temporary Workaround

If custom template is causing issues, temporarily disable it:

1. Rename `backend/templates/registration/login.html` to `login.html.bak`
2. Redeploy
3. Test admin login
4. If it works, the issue is in the custom template

---

## Most Likely Causes (Based on Common Issues)

1. **Static files not collected** - 40% probability
2. **Template syntax error** - 30% probability  
3. **Database connection issue** - 20% probability
4. **Import error** - 10% probability

---

## Immediate Action Required

**Check Render Logs NOW** - This will show the exact error causing the 500.

Go to: Render Dashboard → myshp-backend → Logs → Look for recent errors

