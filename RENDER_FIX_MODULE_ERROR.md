# Fix Render ModuleNotFoundError: No module named 'app'

## Problem
Render is trying to import 'app' instead of 'edithclothes.wsgi:application'

## Solution

### Option 1: Update Render Dashboard Settings (RECOMMENDED)

1. Go to **Render Dashboard**: https://dashboard.render.com
2. Click on your service: **myshp-backend**
3. Go to **Settings** tab
4. Scroll to **Build & Deploy** section
5. Update these settings:

   **Root Directory:**
   ```
   backend
   ```

   **Start Command:**
   ```
   bash start.sh
   ```
   
   OR directly use:
   ```
   gunicorn edithclothes.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120
   ```

6. Click **Save Changes**
7. Go to **Manual Deploy** → **Deploy latest commit**

### Option 2: Verify render.yaml is Applied

If using `render.yaml`:
1. Make sure `render.yaml` is in the **root** of your repository (not in backend/)
2. Render should automatically detect it
3. If not, manually apply settings from Option 1

### Option 3: Direct Gunicorn Command

If the above doesn't work, set Start Command directly in Render dashboard to:
```
cd backend && gunicorn edithclothes.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120
```

## Verify Configuration

After updating, check the logs. You should see:
- ✅ Current directory shows `/opt/render/project/src/backend` or similar
- ✅ Gunicorn starting with `edithclothes.wsgi:application`
- ✅ No `ModuleNotFoundError`

## Current Configuration Files

- `backend/start.sh` - Contains correct Gunicorn command
- `backend/Procfile` - Uses start.sh
- `backend/render.yaml` - Has `rootDir: backend` and `startCommand: bash start.sh`

## Important Notes

- The `rootDir: backend` in render.yaml tells Render where your Django project is
- The start.sh script ensures we're in the right directory
- If Render dashboard settings override render.yaml, update the dashboard manually

