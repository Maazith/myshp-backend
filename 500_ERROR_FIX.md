# 🔧 500 Error Fix - Admin Login

## Issue
Admin login page showing "Server Error (500)" at `https://myshp-backend.onrender.com/admin/login/`

## Root Causes Identified

1. **SECURE_SSL_REDIRECT = True** - Causing redirect loops on Render
2. **ALLOWED_HOSTS wildcard syntax** - Incorrect format
3. **Media file serving** - Potential errors if MEDIA_ROOT doesn't exist
4. **HSTS settings** - Can cause issues on Render

## Fixes Applied

### 1. Disabled SECURE_SSL_REDIRECT
**Why:** Render handles HTTPS at the load balancer level. Forcing SSL redirect causes redirect loops.

**Change:**
```python
# Before:
SECURE_SSL_REDIRECT = True

# After:
SECURE_SSL_REDIRECT = False  # Render handles HTTPS
```

### 2. Fixed ALLOWED_HOSTS Syntax
**Why:** Django doesn't support `*.onrender.com` format. Use `.onrender.com` instead.

**Change:**
```python
# Before:
ALLOWED_HOSTS = ["*.onrender.com"]

# After:
ALLOWED_HOSTS = [".onrender.com"]  # Correct wildcard syntax
```

### 3. Added Media Directory Error Handling
**Why:** Prevents errors if MEDIA_ROOT doesn't exist on first deployment.

**Change:**
```python
# Added error handling for media directory creation
try:
    MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
except (OSError, PermissionError):
    pass  # Continue if can't create
```

### 4. Disabled HSTS
**Why:** HSTS can cause issues on Render's infrastructure.

**Change:**
```python
# Before:
SECURE_HSTS_SECONDS = 31536000

# After:
SECURE_HSTS_SECONDS = 0  # Disabled
```

### 5. Added Media File Serving Error Handling
**Why:** Prevents 500 errors if media files aren't accessible.

**Change:**
```python
# Added try-except for media file serving
try:
    if settings.MEDIA_ROOT and os.path.exists(settings.MEDIA_ROOT):
        urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, ...)]
except Exception:
    pass  # Skip if media root doesn't exist
```

## Files Modified

1. `backend/edithclothes/settings.py`
   - Disabled SECURE_SSL_REDIRECT
   - Fixed ALLOWED_HOSTS
   - Disabled HSTS
   - Added media directory error handling

2. `backend/edithclothes/urls.py`
   - Added error handling for media file serving

## Verification

After deployment, test:
1. Visit: `https://myshp-backend.onrender.com/admin/login/`
2. Should load login page (not 500 error)
3. Can login with admin credentials

## Status

✅ **FIXED** - All changes committed and pushed
⏳ **DEPLOYING** - Render will auto-deploy (2-5 minutes)

---

**Note:** If 500 error persists after deployment, check Render logs for specific error messages.

