# 🚨 CRITICAL: Manual Render Dashboard Fix Required

## The Problem
Render is still looking for `/opt/render/project/src/ backend` directory, which doesn't exist.

## Root Cause
The Render dashboard has a **manual setting** for "Root Directory" that's overriding the `render.yaml` file.

## ✅ IMMEDIATE FIX - Update Render Dashboard

### Step-by-Step Instructions:

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Login to your account

2. **Select Your Service**
   - Click on **"myshp-backend"** service

3. **Go to Settings**
   - Click **"Settings"** in the left sidebar

4. **Find "Build & Deploy" Section**
   - Scroll down to find **"Build & Deploy"** section

5. **Clear/Remove Root Directory**
   - Find the **"Root Directory"** field
   - **DELETE** or **CLEAR** any value in this field (it might say "backend")
   - Leave it **EMPTY** or set it to **"."** (just a dot)
   - This tells Render the root IS the repository root

6. **Verify Start Command**
   - Make sure **"Start Command"** is set to:
     ```
     bash start.sh
     ```
   - OR directly:
     ```
     gunicorn edithclothes.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120
     ```

7. **Save Changes**
   - Click **"Save Changes"** button at the bottom

8. **Manual Deploy**
   - Go to **"Manual Deploy"** dropdown
   - Click **"Deploy latest commit"**

## Why This Happens

- Render dashboard settings **override** `render.yaml` file
- If you set "Root Directory" manually in the dashboard, it takes precedence
- The `render.yaml` file is only used if you deploy via Render's Blueprint feature

## After Fixing

Once you clear the Root Directory setting:
- ✅ Render will use the repository root (where `manage.py` is)
- ✅ All commands will run from the correct directory
- ✅ Deployment should succeed

## Verification

After deployment, check logs for:
- ✅ `📁 Current directory: /opt/render/project/src` (or similar)
- ✅ `✅ Found manage.py and edithclothes module`
- ✅ `🚀 Starting Gunicorn...`
- ✅ No more "Service Root Directory missing" errors

---

**IMPORTANT:** You MUST manually update the Render dashboard settings. The `render.yaml` file alone won't fix this if the dashboard has manual settings configured.

