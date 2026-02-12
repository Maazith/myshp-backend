# PostgreSQL Migration Guide

## Overview
This guide will help you migrate from SQLite to PostgreSQL for both local development and Render deployment.

---

## Step 1: Install PostgreSQL Locally

### Option A: Using Docker (Recommended - Easy Setup)

If you want to use Docker, we can generate a `docker-compose.yaml` file. **Do you want Docker setup?**

If yes, run:
```bash
docker-compose up -d
```

This will start PostgreSQL automatically.

### Option B: Install PostgreSQL Directly

**Windows:**
1. Download PostgreSQL from https://www.postgresql.org/download/windows/
2. Install with default settings
3. Remember the password you set for the `postgres` user

**macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

---

## Step 2: Create Local PostgreSQL Database

1. **Open PostgreSQL command line** (psql) or pgAdmin

2. **Create database and user:**
```sql
-- Connect as postgres superuser
psql -U postgres

-- Create database
CREATE DATABASE myshp_db;

-- Create user (optional, or use existing postgres user)
CREATE USER devuser WITH PASSWORD 'devpass';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE myshp_db TO devuser;

-- Exit
\q
```

3. **Update `.env` file** with your database credentials:
```bash
# In backend/backend/backend/.env
DATABASE_URL=postgres://devuser:devpass@localhost:5432/myshp_db
```

---

## Step 3: Backup Existing SQLite Data (Optional but Recommended)

If you have important data in SQLite that you want to keep:

```bash
# Navigate to backend directory
cd backend/backend/backend

# Export data to JSON
python manage.py dumpdata > backup_data.json

# Keep this file safe! You can import it later if needed.
```

---

## Step 4: Delete Old SQLite Database

**⚠️ IMPORTANT: Only delete after confirming backup or if you're okay losing existing data!**

```bash
# Navigate to backend directory
cd backend/backend/backend

# Delete SQLite database (only if you're sure!)
# Windows:
del db.sqlite3

# macOS/Linux:
rm db.sqlite3
```

---

## Step 5: Run Migrations on PostgreSQL

```bash
# Make sure you're in the backend directory
cd backend/backend/backend

# Create new migrations (if any model changes)
python manage.py makemigrations

# Apply migrations to PostgreSQL
python manage.py migrate
```

You should see output like:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, shop
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

---

## Step 6: Create Superuser for PostgreSQL

```bash
# Create admin user
python manage.py createsuperuser

# Follow prompts:
# Username: admin
# Email: admin@edithcloths.com
# Password: [enter strong password]
```

---

## Step 7: Import Backup Data (If Applicable)

If you backed up data from SQLite:

```bash
# Import data to PostgreSQL
python manage.py loaddata backup_data.json
```

**Note:** This may fail if there are foreign key conflicts. You may need to import in a specific order or clean up the JSON file.

---

## Step 8: Verify Local PostgreSQL Connection

```bash
# Test database connection
python manage.py dbshell

# You should see PostgreSQL prompt:
# myshp_db=>

# Try a simple query:
SELECT version();

# Exit:
\q
```

---

## Step 9: Test Your Application Locally

1. **Start development server:**
```bash
python manage.py runserver
```

2. **Test admin login:**
   - Go to http://127.0.0.1:8000/edith-admin-login/
   - Login with superuser credentials
   - Verify you can access admin panel

3. **Test API endpoints:**
   - http://127.0.0.1:8000/api/products/
   - http://127.0.0.1:8000/api/orders/
   - Verify data loads correctly

---

## Step 10: Render Deployment Setup

### A. Environment Variables in Render

1. **Go to Render Dashboard** → Your backend service (`myshp-backend`)

2. **Navigate to Environment** → Environment Variables

3. **Verify/Set these variables:**

   **Required:**
   - `DATABASE_URL` = [Auto-set by Render when database is linked]
   - `RENDER` = `true`
   - `ENVIRONMENT` = `production`
   - `DEBUG` = `False`
   - `SECRET_KEY` = [Generated key]

   **Database Link:**
   - In Render dashboard, go to your web service
   - Click "Link Database" or verify database is linked
   - Render will automatically set `DATABASE_URL`

### B. Run Migrations on Render

**Option 1: Using Render Shell (Recommended)**

1. Go to Render Dashboard → Your backend service
2. Click "Shell" tab
3. Run:
```bash
python manage.py migrate
python manage.py createsuperuser
```

**Option 2: Using Render Logs**

Migrations should run automatically if you have them in your `start.sh` script. Check `start.sh` to verify:

```bash
python manage.py migrate --noinput
```

### C. Verify Render Deployment

1. **Check Render logs** for:
   - "Operations to perform: Apply all migrations"
   - "Running migrations: ... OK"
   - No database connection errors

2. **Test API endpoints:**
   - https://myshp-backend.onrender.com/api/products/
   - https://myshp-backend.onrender.com/api/orders/

3. **Test admin login:**
   - https://myshp-backend.onrender.com/edith-admin-login/
   - Login with superuser credentials

---

## Troubleshooting

### Error: "could not connect to server"

**Local:**
- Check PostgreSQL is running: `pg_isready` or `docker ps`
- Verify DATABASE_URL in `.env` is correct
- Check PostgreSQL port (default: 5432)

**Render:**
- Verify database is linked to web service
- Check `DATABASE_URL` environment variable is set
- Check Render database status (should be "Available")

### Error: "relation does not exist"

**Solution:**
```bash
python manage.py migrate
```

### Error: "password authentication failed"

**Local:**
- Check `.env` file has correct password
- Verify PostgreSQL user exists and has correct password

**Render:**
- Verify `DATABASE_URL` is correct (auto-set by Render)

### Error: "database does not exist"

**Local:**
- Create database: `CREATE DATABASE myshp_db;`
- Update `.env` with correct database name

**Render:**
- Verify database is created in Render dashboard
- Check database name matches connection string

---

## Final Verification Checklist

### Local Development:
- [ ] PostgreSQL is running
- [ ] `.env` file exists with correct `DATABASE_URL`
- [ ] `db.sqlite3` is deleted (or backed up)
- [ ] Migrations run successfully: `python manage.py migrate`
- [ ] Superuser created: `python manage.py createsuperuser`
- [ ] Admin login works: http://127.0.0.1:8000/edith-admin-login/
- [ ] API endpoints work: http://127.0.0.1:8000/api/products/
- [ ] No SQLite references in code (except fallback)

### Render Deployment:
- [ ] Database is linked to web service
- [ ] `DATABASE_URL` environment variable is set (auto-set by Render)
- [ ] Migrations run successfully (check logs)
- [ ] Superuser created (via shell or management command)
- [ ] Admin login works: https://myshp-backend.onrender.com/edith-admin-login/
- [ ] API endpoints work: https://myshp-backend.onrender.com/api/products/
- [ ] No database connection errors in logs

---

## Docker Setup (Optional)

If you want to use Docker for local PostgreSQL, I can generate a `docker-compose.yaml` file. **Would you like me to create it?**

The docker-compose.yaml would include:
- PostgreSQL 15 container
- Pre-configured database, user, and password
- Volume for data persistence
- Port mapping (5432:5432)

Let me know if you want Docker setup!

---

## Next Steps After Migration

1. **Update `.gitignore`** to include `.env` (if not already):
```
.env
*.sqlite3
db.sqlite3
```

2. **Test all functionality:**
   - Product creation
   - Order processing
   - Admin panel
   - API endpoints

3. **Monitor performance:**
   - PostgreSQL should be faster than SQLite
   - Check query performance in admin panel

4. **Backup strategy:**
   - Set up regular PostgreSQL backups
   - Render provides automatic backups for paid plans

---

## Need Help?

If you encounter issues:
1. Check error messages in console/logs
2. Verify environment variables are set correctly
3. Ensure PostgreSQL is running (local)
4. Verify database connection string format
5. Check Render logs for deployment issues










