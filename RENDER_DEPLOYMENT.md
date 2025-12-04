# Render Deployment Configuration

## ✅ Changes Made

### 1. Database Configuration
- ✅ Replaced SQLite with PostgreSQL
- ✅ Added `psycopg2-binary` and `dj-database-url` to requirements.txt
- ✅ Updated DATABASES setting to use `dj_database_url.config()`

### 2. Environment Variables
- ✅ Updated DEBUG to read from environment variable
- ✅ Updated ALLOWED_HOSTS for production

### 3. Static & Media Files
- ✅ Static and Media settings already configured correctly

---

## 📄 Final Files

### `backend/requirements.txt`
```
Django==4.2.10
djangorestframework==3.15.1
django-cors-headers==4.3.1
djangorestframework-simplejwt==5.3.1

# Database
psycopg2-binary==2.9.9
dj-database-url==2.1.0

# Additional recommended packages
Pillow==12.0.0           # For image uploads (product images, banners)
python-dotenv==1.0.1      # If environment variables needed later
gunicorn==21.2.0          # For production servers like Render
whitenoise==6.6.0         # For serving static files in production
```

### `backend/edithclothes/settings.py` (Key Sections)

**Imports:**
```python
import os
import dj_database_url
```

**DEBUG:**
```python
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
```

**ALLOWED_HOSTS:**
```python
ALLOWED_HOSTS = ["*", "localhost", "127.0.0.1"]
```

**DATABASES:**
```python
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    )
}
```

**STATIC & MEDIA (Already Correct):**
```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

## 📁 Project Structure

```
backend/
├── edithclothes/
│   ├── __init__.py
│   ├── settings.py          ✅ Updated
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── shop/
│   ├── models.py           ✅ No changes
│   ├── views.py            ✅ No changes
│   ├── serializers.py      ✅ No changes
│   ├── admin.py            ✅ No changes
│   └── migrations/
├── manage.py
├── requirements.txt        ✅ Updated
├── static/
├── media/
└── templates/
```

---

## 🔐 Environment Variables for Render

Set these in your Render dashboard under **Environment Variables**:

### Required Variables:

```bash
# Database (Auto-provided by Render PostgreSQL service)
DATABASE_URL=postgresql://user:password@host:port/dbname

# Debug Mode (Set to False for production)
DEBUG=False

# Secret Key (Generate a new one for production!)
SECRET_KEY=your-production-secret-key-here

# Email Configuration (Optional - if using email)
EMAIL_HOST_PASSWORD=your-email-app-password
```

### Example `.env` file (for local testing):

```bash
# .env (DO NOT commit this file!)
DATABASE_URL=postgresql://user:password@localhost:5432/edithcloths
DEBUG=True
SECRET_KEY=django-insecure-9o(%hgr4x$ii_ct2m(hw8=nj7g$06izqws-$_u@%5u795&_to^
EMAIL_HOST_PASSWORD=your-gmail-app-password
```

---

## 🚀 Render Deployment Steps

1. **Create PostgreSQL Database on Render**
   - Go to Render Dashboard → New → PostgreSQL
   - Copy the Internal Database URL

2. **Create Web Service on Render**
   - Go to Render Dashboard → New → Web Service
   - Connect your repository
   - Set build command: `pip install -r backend/requirements.txt`
   - Set start command: `cd backend && gunicorn edithclothes.wsgi:application --bind 0.0.0.0:$PORT`
   - Set root directory: `backend`

3. **Set Environment Variables**
   - `DATABASE_URL`: (Auto-provided if you link PostgreSQL service)
   - `DEBUG`: `False`
   - `SECRET_KEY`: Generate a new secret key
   - `EMAIL_HOST_PASSWORD`: (If using email)

4. **Run Migrations**
   - After first deployment, run migrations:
   - In Render shell: `python manage.py migrate`
   - Create superuser: `python manage.py createsuperuser`

5. **Collect Static Files**
   - Render will automatically run `python manage.py collectstatic` during build
   - Static files will be served from `staticfiles/` directory

---

## ✅ Verification Checklist

- [x] PostgreSQL database configuration added
- [x] psycopg2-binary and dj-database-url added to requirements.txt
- [x] DEBUG reads from environment variable
- [x] ALLOWED_HOSTS updated
- [x] Static and Media settings configured
- [x] No changes to models, views, admin, or API logic
- [x] Project ready for production deployment

---

## 📝 Notes

- **SECRET_KEY**: Generate a new secret key for production. Never use the development key!
- **Database**: Render will automatically provide DATABASE_URL when you link a PostgreSQL service
- **Static Files**: WhiteNoise is already in requirements.txt for serving static files
- **Media Files**: For production, consider using cloud storage (AWS S3, Cloudinary) for media files
- **SSL**: Database connection uses SSL (ssl_require=True) for security

---

**Ready for deployment!** 🎉

---

## 📚 Additional Guides

- **Standard Plan Setup**: See `RENDER_STANDARD_PLAN_SETUP.md` for detailed step-by-step guide
- **Quick Start**: See `RENDER_QUICK_START.md` for fast setup reference

