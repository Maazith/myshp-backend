# ⚡ Render Quick Start

## 🎯 Quick Setup (5 Minutes)

### Option 1: Free Plan (Testing) 🆓
**Recommended for initial testing**

### 1. Create PostgreSQL Database
```
New + → PostgreSQL
Name: edithcloths-db
Plan: Free
Create Database
```

### 2. Create Web Service
```
New + → Web Service
Repository: Maazith/myshp-backend
Build Command: pip install -r requirements.txt && python manage.py collectstatic --noinput
Start Command: gunicorn edithclothes.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120
Instance: Free ($0/month) - For testing
```

### Option 2: Standard Plan (Production) 💼
**Recommended for production**

### 2. Create Web Service
```
New + → Web Service
Repository: Maazith/myshp-backend
Build Command: pip install -r requirements.txt && python manage.py collectstatic --noinput
Start Command: gunicorn edithclothes.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
Instance: Standard ($25/month) - For production
```

### 3. Environment Variables
```
DEBUG=False
SECRET_KEY=<generate-new-key>
DATABASE_URL=<link-database-or-paste-url>
```

### 4. Deploy & Migrate
```
Deploy → Wait for build → Shell → python manage.py migrate → createsuperuser
```

---

## 📋 Copy-Paste Commands

### Build Command:
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

### Start Command:
```bash
gunicorn edithclothes.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

### Generate Secret Key:
```python
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

---

## ✅ Checklist

- [ ] PostgreSQL database created
- [ ] Web service created (Standard plan)
- [ ] Environment variables set
- [ ] Database linked to web service
- [ ] First deployment successful
- [ ] Migrations run
- [ ] Superuser created
- [ ] API tested

---

**Full guide**: See `RENDER_STANDARD_PLAN_SETUP.md` for detailed instructions.

