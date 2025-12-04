# 🆓 Render Free Plan Testing Guide

## Overview
This guide helps you test your Django backend on Render's **Free Plan** before upgrading to Standard.

---

## ⚠️ Free Plan Limitations

### Resources:
- **RAM**: 512 MB (limited)
- **CPU**: 0.1 CPU (very limited)
- **Workers**: 1 Gunicorn worker (optimized for free tier)

### Service Behavior:
- ⏸️ **Spins down after 15 minutes of inactivity**
- 🐌 **Slower cold starts** (30-60 seconds after spin-down)
- ❌ **No zero downtime deployments**
- ⚠️ **May experience timeouts** under heavy load
- 📊 **Limited monitoring** compared to paid plans

### What This Means:
- ✅ **Good for**: Testing, development, low-traffic demos
- ❌ **Not ideal for**: Production, high traffic, real customers
- 💡 **Recommendation**: Test on free, upgrade to Standard ($25/month) for production

---

## 🚀 Quick Setup (Free Plan)

### Step 1: Create PostgreSQL Database (Free)
1. Render Dashboard → **New +** → **PostgreSQL**
2. **Name**: `edithcloths-db`
3. **Plan**: **Free** ✅
4. **Create Database**

### Step 2: Create Web Service (Free)
1. Render Dashboard → **New +** → **Web Service**
2. Connect repository: `Maazith/myshp-backend`
3. Configure:
   - **Name**: `edithcloths-backend`
   - **Environment**: Python 3
   - **Plan**: **Free** ✅
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && python manage.py collectstatic --noinput
     ```
   - **Start Command**: 
     ```bash
     gunicorn edithclothes.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120
     ```

### Step 3: Environment Variables
```
DEBUG=False
SECRET_KEY=<generate-new-key>
DATABASE_URL=<link-database>
```

### Step 4: Link Database
- In Web Service → **Environment** tab
- Click **"Link Database"** → Select `edithcloths-db`

### Step 5: Deploy & Test
- Wait for build (3-5 minutes)
- Run migrations: `python manage.py migrate`
- Create superuser: `python manage.py createsuperuser`
- Test your API endpoints

---

## 🧪 Testing Checklist

### Basic Functionality:
- [ ] Service deploys successfully
- [ ] API endpoints respond (may be slow on first request)
- [ ] Database migrations run
- [ ] Admin panel accessible
- [ ] Static files load correctly

### Performance Testing:
- [ ] First request after spin-down (cold start): ~30-60 seconds
- [ ] Subsequent requests: Should be faster
- [ ] Multiple concurrent requests: May timeout
- [ ] Image uploads: May be slow

### Limitations Testing:
- [ ] Wait 15+ minutes → Service spins down
- [ ] Make request → Service spins up (takes time)
- [ ] Check memory usage (should stay under 512MB)

---

## 📊 Expected Performance

### Free Plan:
- **Cold Start**: 30-60 seconds (after 15 min inactivity)
- **Response Time**: 1-3 seconds (after warm-up)
- **Concurrent Users**: 1-5 users max
- **Memory Usage**: ~300-450 MB (Django + PostgreSQL connections)

### When to Upgrade:
- ✅ If service works but is slow → Upgrade to Standard
- ✅ If you get memory errors → Upgrade to Standard
- ✅ If you need production → Upgrade to Standard
- ✅ If traffic increases → Upgrade to Standard

---

## 🔄 Upgrading to Standard Plan

When ready to upgrade:

1. **In Render Dashboard**:
   - Go to your Web Service
   - Click **"Settings"** → **"Instance Type"**
   - Select **Standard** ($25/month)
   - Click **"Save Changes"**

2. **Update Start Command**:
   - Change workers from `1` to `2`:
   ```bash
   gunicorn edithclothes.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
   ```

3. **Redeploy**:
   - Render will automatically redeploy with new resources

---

## 🐛 Troubleshooting Free Plan Issues

### Service Keeps Spinning Down
- **Cause**: 15-minute inactivity timeout
- **Solution**: This is normal. First request will wake it up (takes time)

### Slow Response Times
- **Cause**: Limited CPU (0.1 CPU)
- **Solution**: Expected on free plan. Upgrade to Standard for better performance

### Memory Errors
- **Cause**: Exceeding 512 MB RAM
- **Solution**: 
  - Reduce Gunicorn workers (already set to 1)
  - Upgrade to Standard plan

### Timeouts
- **Cause**: Limited resources
- **Solution**: 
  - Increase timeout in start command (already 120 seconds)
  - Upgrade to Standard plan

### Build Failures
- **Cause**: Memory limits during build
- **Solution**: 
  - Ensure `collectstatic` runs with `--noinput` flag ✅
  - Check build logs for specific errors

---

## 💰 Cost Comparison

| Plan | Monthly Cost | RAM | CPU | Workers | Best For |
|------|-------------|-----|-----|---------|----------|
| **Free** | $0 | 512 MB | 0.1 | 1 | Testing |
| **Standard** | $25 | 2 GB | 1 | 2 | Production |

---

## ✅ Free Plan Configuration Summary

### Current Settings (Optimized for Free):
- ✅ Plan: **Free**
- ✅ Workers: **1** (reduced from 2)
- ✅ Timeout: **120 seconds**
- ✅ Static files: **WhiteNoise** (compressed)
- ✅ Database: **Free PostgreSQL**

### Files Updated:
- ✅ `render.yaml` - Free plan configured
- ✅ `Procfile` - 1 worker for free tier
- ✅ `settings.py` - Already optimized

---

## 🎯 Next Steps

1. **Deploy on Free Plan** → Test functionality
2. **Verify Everything Works** → Check all endpoints
3. **Monitor Performance** → Check response times
4. **Decide on Upgrade** → Based on your needs
5. **Upgrade to Standard** → When ready for production

---

## 📝 Notes

- **Free plan is perfect for testing** before committing to paid plan
- **No credit card required** for free tier
- **Easy upgrade path** - just change instance type
- **All your data preserved** when upgrading

---

**Ready to test on Free Plan!** 🆓

After testing, you can easily upgrade to Standard ($25/month) for production use.

