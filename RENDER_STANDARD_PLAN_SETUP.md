# 🚀 Render Standard Plan Deployment Guide

## Overview
This guide will help you deploy your Django backend to Render using the **Standard Plan ($25/month)**.

---

## 📋 Prerequisites

- ✅ GitHub repository pushed (already done: `Maazith/myshp-backend`)
- ✅ Render account created
- ✅ Credit card added to Render account

---

## 🗄️ Step 1: Create PostgreSQL Database

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `edithcloths-db`
   - **Database**: `edithcloths`
   - **User**: `edithcloths_user`
   - **Plan**: **Free** (you can upgrade later if needed)
   - **Region**: Choose closest to your users
4. Click **"Create Database"**
5. **Important**: Copy the **Internal Database URL** (you'll need it later)
   - Format: `postgresql://user:password@host:port/dbname`

---

## 🌐 Step 2: Create Web Service (Standard Plan)

1. In Render Dashboard, click **"New +"** → **"Web Service"**
2. Connect your repository:
   - Click **"Connect account"** if not connected
   - Select **"GitHub"** → Authorize Render
   - Find and select: **`Maazith/myshp-backend`**
   - Click **"Connect"**

3. Configure the service:
   - **Name**: `edithcloths-backend`
   - **Environment**: **Python 3**
   - **Region**: Same as database (for lower latency)
   - **Branch**: `main`
   - **Root Directory**: Leave empty (or set to `.` if needed)
   - **Runtime**: `Python 3.11` or `Python 3.12`

4. **Build & Start Commands**:
   ```
   Build Command:
   pip install -r requirements.txt && python manage.py collectstatic --noinput
   
   Start Command:
   gunicorn edithclothes.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
   ```

5. **Instance Type**: Select **Standard** ($25/month)
   - 2 GB RAM
   - 1 CPU
   - Zero downtime deployments

6. Click **"Create Web Service"**

---

## 🔐 Step 3: Configure Environment Variables

In your Web Service dashboard, go to **"Environment"** tab and add:

### Required Variables:

```bash
# Database (Link to PostgreSQL service)
DATABASE_URL=postgresql://user:password@host:port/dbname
# OR: Click "Link Database" and select edithcloths-db (auto-fills)

# Debug Mode (MUST be False for production)
DEBUG=False

# Secret Key (Generate a new one!)
SECRET_KEY=your-unique-secret-key-here-min-50-characters
```

**To generate SECRET_KEY:**
```python
# Run this in Python:
import secrets
print(secrets.token_urlsafe(50))
```

### Optional Variables (if using email):

```bash
# Email Configuration
EMAIL_HOST_PASSWORD=your-gmail-app-password
EMAIL_HOST_USER=maazith.md@gmail.com
DEFAULT_FROM_EMAIL=maazith.md@gmail.com
ADMIN_EMAIL=maazith.md@gmail.com
```

### How to Add Variables:
1. Go to your Web Service → **"Environment"** tab
2. Click **"Add Environment Variable"**
3. Enter **Key** and **Value**
4. Click **"Save Changes"**

---

## 🔗 Step 4: Link Database to Web Service

1. In your Web Service dashboard
2. Go to **"Environment"** tab
3. Scroll to **"Linked Databases"** section
4. Click **"Link Database"**
5. Select **`edithcloths-db`**
6. Render will automatically add `DATABASE_URL` environment variable

---

## 🚀 Step 5: Deploy

1. After saving environment variables, Render will automatically start building
2. Watch the build logs:
   - Should see: "Installing dependencies..."
   - Should see: "Collecting static files..."
   - Should see: "Build complete!"
3. First deployment takes 3-5 minutes

---

## 📊 Step 6: Run Database Migrations

After first successful deployment:

1. Go to your Web Service dashboard
2. Click **"Shell"** tab (or use Render Shell)
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```
   - Enter username, email, and password

---

## ✅ Step 7: Verify Deployment

1. **Check Service Status**:
   - Should show: **"Live"** (green)
   - URL: `https://edithcloths-backend.onrender.com` (or your custom domain)

2. **Test API Endpoints**:
   ```bash
   # Health check
   curl https://your-service.onrender.com/api/
   
   # Products
   curl https://your-service.onrender.com/api/products/
   ```

3. **Test Admin Panel**:
   - Visit: `https://your-service.onrender.com/admin/`
   - Login with superuser credentials

---

## 📝 Configuration Files Created

### `render.yaml` (Optional - for Infrastructure as Code)
- Defines services and databases
- Can be used for automated setup

### `Procfile` (Start command)
- Defines how to start the application
- Used by Render if no start command specified

### `build.sh` (Build script)
- Custom build steps
- Can be referenced in build command

---

## 🔧 Standard Plan Settings Explained

### Gunicorn Workers
- **2 workers**: Optimal for Standard plan (1 CPU)
- Formula: `(2 × CPU cores) + 1` = 2 workers for 1 CPU
- Handles concurrent requests efficiently

### Timeout
- **120 seconds**: Prevents long-running requests from timing out
- Good for image uploads and processing

### Static Files
- WhiteNoise middleware configured
- Static files compressed and cached
- Served efficiently in production

---

## 💰 Cost Breakdown

- **Web Service (Standard)**: $25/month
- **PostgreSQL (Free)**: $0/month
- **Total**: **$25/month**

*Note: Free PostgreSQL has limitations. Upgrade to Starter ($7/month) if you need more storage/connections.*

---

## 🐛 Troubleshooting

### Build Fails
- Check build logs for errors
- Verify `requirements.txt` is correct
- Ensure Python version is compatible

### Database Connection Error
- Verify `DATABASE_URL` is set correctly
- Check database is running
- Ensure database is linked to web service

### Static Files Not Loading
- Verify `collectstatic` ran successfully
- Check WhiteNoise middleware is in settings
- Verify `STATIC_ROOT` is set correctly

### 500 Internal Server Error
- Check application logs
- Verify `DEBUG=False` in production
- Check database migrations ran
- Verify SECRET_KEY is set

### Service Crashes
- Check memory usage (Standard plan: 2GB)
- Review application logs
- Verify gunicorn workers count (2 is optimal)

---

## 📈 Monitoring & Scaling

### Monitor Your Service:
- **Metrics**: CPU, Memory, Request Rate
- **Logs**: Real-time application logs
- **Events**: Deployments, restarts, errors

### When to Upgrade:
- **Memory**: If using >80% consistently
- **CPU**: If CPU usage is consistently high
- **Traffic**: If handling >1000 requests/minute

### Scaling Options:
- **Vertical**: Upgrade to Pro plan ($85/month)
- **Horizontal**: Add more instances (Pro plan required)

---

## 🔒 Security Checklist

- [x] `DEBUG=False` in production
- [x] Strong `SECRET_KEY` set
- [x] Database uses SSL (`ssl_require=True`)
- [x] `ALLOWED_HOSTS` configured
- [x] CORS settings configured
- [ ] HTTPS enabled (automatic on Render)
- [ ] Environment variables secured (not in code)

---

## 🎯 Next Steps

1. ✅ Deploy backend to Render
2. ⏭️ Update frontend API URL to point to Render backend
3. ⏭️ Test full application flow
4. ⏭️ Set up custom domain (optional)
5. ⏭️ Configure email service
6. ⏭️ Set up monitoring alerts

---

## 📞 Support

- **Render Docs**: https://render.com/docs
- **Render Status**: https://status.render.com
- **Django Deployment**: https://docs.djangoproject.com/en/stable/howto/deployment/

---

**Your Django backend is now ready for production on Render Standard Plan!** 🎉

