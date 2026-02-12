# PostgreSQL Migration - Setup Summary

## ✅ Changes Made

### 1. **requirements.txt** ✅
- Updated `dj-database-url` from `2.1.0` to `2.2.0`
- `psycopg2-binary==2.9.9` already present ✅

### 2. **settings.py** ✅
- Added `from dotenv import load_dotenv` and `load_dotenv()` for .env file support
- Updated database configuration to use PostgreSQL with `dj_database_url.parse()`
- Added SQLite fallback when `DATABASE_URL` is not set
- Added `ATOMIC_REQUESTS = True` for PostgreSQL (best practice)
- Kept `TIME_ZONE = 'UTC'` and `USE_TZ = True` (unchanged)

### 3. **Environment Files** ✅
- Created `env.example` template file
- Instructions for creating `.env` file (user needs to create manually)

### 4. **Docker Support** ✅
- Created `docker-compose.yaml` for optional Docker PostgreSQL setup

### 5. **Documentation** ✅
- Created `POSTGRESQL_MIGRATION_GUIDE.md` with complete step-by-step instructions

---

## 📋 Next Steps for You

### Step 1: Create `.env` File (Local Development)

1. Copy `env.example` to `.env`:
```bash
cd backend/backend/backend
copy env.example .env  # Windows
# OR
cp env.example .env   # macOS/Linux
```

2. Edit `.env` and update `DATABASE_URL`:
```
DATABASE_URL=postgres://devuser:devpass@localhost:5432/myshp_db
```

**Important:** Adjust username, password, and database name to match your PostgreSQL setup!

### Step 2: Install PostgreSQL Locally

**Option A: Use Docker (Easiest)**
```bash
cd backend/backend/backend
docker-compose up -d
```

**Option B: Install PostgreSQL Directly**
- Windows: Download from https://www.postgresql.org/download/windows/
- macOS: `brew install postgresql@15`
- Linux: `sudo apt install postgresql`

### Step 3: Create PostgreSQL Database

```sql
-- Connect to PostgreSQL
psql -U postgres

-- Create database
CREATE DATABASE myshp_db;

-- Create user (if using Docker, user already exists)
CREATE USER devuser WITH PASSWORD 'devpass';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE myshp_db TO devuser;

-- Exit
\q
```

### Step 4: Backup & Migrate

```bash
cd backend/backend/backend

# 1. Backup existing SQLite data (optional)
python manage.py dumpdata > backup_data.json

# 2. Delete SQLite database (only if you're sure!)
del db.sqlite3  # Windows
# OR
rm db.sqlite3   # macOS/Linux

# 3. Run migrations
python manage.py makemigrations
python manage.py migrate

# 4. Create superuser
python manage.py createsuperuser
```

### Step 5: Test Locally

```bash
# Start server
python manage.py runserver

# Test:
# - Admin login: http://127.0.0.1:8000/edith-admin-login/
# - API: http://127.0.0.1:8000/api/products/
```

### Step 6: Render Deployment

1. **Verify Environment Variables:**
   - Go to Render Dashboard → Your backend service
   - Check `DATABASE_URL` is set (auto-set when database is linked)

2. **Link Database (if not already):**
   - In Render dashboard, link PostgreSQL database to web service
   - Render will automatically set `DATABASE_URL`

3. **Run Migrations on Render:**
   - Go to Render Shell
   - Run: `python manage.py migrate`
   - Run: `python manage.py createsuperuser`

4. **Verify Deployment:**
   - Check logs for migration success
   - Test admin login: https://myshp-backend.onrender.com/edith-admin-login/
   - Test API: https://myshp-backend.onrender.com/api/products/

---

## 🔍 Verification Checklist

### Local Development:
- [ ] `.env` file created with correct `DATABASE_URL`
- [ ] PostgreSQL is running (check with `pg_isready` or `docker ps`)
- [ ] Database `myshp_db` exists
- [ ] `db.sqlite3` deleted (or backed up)
- [ ] Migrations run: `python manage.py migrate` ✅
- [ ] Superuser created: `python manage.py createsuperuser` ✅
- [ ] Admin login works ✅
- [ ] API endpoints work ✅

### Render Deployment:
- [ ] Database linked to web service ✅
- [ ] `DATABASE_URL` environment variable set (auto-set) ✅
- [ ] Migrations run successfully (check logs) ✅
- [ ] Superuser created ✅
- [ ] Admin login works ✅
- [ ] API endpoints work ✅

---

## 📝 Important Notes

1. **`.env` file is gitignored** - Never commit it to git!
2. **SQLite fallback** - If `DATABASE_URL` is not set, Django will use SQLite (for safety)
3. **Render auto-sets DATABASE_URL** - When you link a database in Render, it automatically sets the `DATABASE_URL` environment variable
4. **ATOMIC_REQUESTS** - Enabled for PostgreSQL (each HTTP request is wrapped in a transaction)
5. **Connection pooling** - `conn_max_age=600` keeps connections alive for 10 minutes

---

## 🐳 Docker Usage (Optional)

If you want to use Docker for local PostgreSQL:

```bash
# Start PostgreSQL
docker-compose up -d

# Check status
docker ps

# Stop PostgreSQL
docker-compose down

# Stop and remove data (careful!)
docker-compose down -v
```

The Docker setup uses:
- PostgreSQL 15
- User: `devuser`
- Password: `devpass`
- Database: `myshp_db`
- Port: `5432`

Update your `.env` file to match:
```
DATABASE_URL=postgres://devuser:devpass@localhost:5432/myshp_db
```

---

## 🆘 Troubleshooting

### "could not connect to server"
- Check PostgreSQL is running: `pg_isready` or `docker ps`
- Verify `.env` file has correct `DATABASE_URL`
- Check PostgreSQL port (default: 5432)

### "database does not exist"
- Create database: `CREATE DATABASE myshp_db;`
- Update `.env` with correct database name

### "password authentication failed"
- Check `.env` file has correct password
- Verify PostgreSQL user exists

### Render: "DATABASE_URL not set"
- Link database to web service in Render dashboard
- Check environment variables in Render

---

## 📚 Files Created/Modified

### Modified:
- ✅ `backend/backend/backend/requirements.txt`
- ✅ `backend/backend/backend/edithclothes/settings.py`

### Created:
- ✅ `backend/backend/backend/env.example`
- ✅ `backend/backend/backend/docker-compose.yaml`
- ✅ `backend/backend/backend/POSTGRESQL_MIGRATION_GUIDE.md`
- ✅ `backend/backend/backend/POSTGRESQL_SETUP_SUMMARY.md` (this file)

---

## ✅ All Requirements Met

- ✅ PostgreSQL dependencies installed (`psycopg2-binary`, `dj-database-url`)
- ✅ Database configuration updated with environment variable support
- ✅ SQLite fallback for safety
- ✅ `.env` file template created
- ✅ Docker support (optional)
- ✅ Migration guide created
- ✅ Render deployment instructions included
- ✅ Verification checklist provided

**You're all set! Follow the steps above to complete the migration.** 🚀










