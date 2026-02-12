# 🚀 PostgreSQL Setup - Next Steps

Since you've installed PostgreSQL, follow these steps:

---

## Step 1: Create PostgreSQL Database

Open **Command Prompt** or **PowerShell** and run:

```bash
# Connect to PostgreSQL (use the password you set during installation)
psql -U postgres
```

Then in the PostgreSQL prompt, run:

```sql
-- Create database
CREATE DATABASE myshp_db;

-- Create user (optional - you can use 'postgres' user if you prefer)
CREATE USER devuser WITH PASSWORD 'devpass';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE myshp_db TO devuser;

-- Exit PostgreSQL
\q
```

**Alternative:** If you installed PostgreSQL with pgAdmin, you can create the database through the GUI.

---

## Step 2: Create .env File

Navigate to your backend directory and create the `.env` file:

```bash
cd backend\backend\backend

# Copy the example file
copy env.example .env
```

Then edit `.env` and update the `DATABASE_URL`:

**If you created a new user:**
```
DATABASE_URL=postgres://devuser:devpass@localhost:5432/myshp_db
```

**If you're using the default 'postgres' user:**
```
DATABASE_URL=postgres://postgres:YOUR_POSTGRES_PASSWORD@localhost:5432/myshp_db
```

Replace `YOUR_POSTGRES_PASSWORD` with the password you set during PostgreSQL installation.

---

## Step 3: Test Database Connection

```bash
cd backend\backend\backend

# Test connection
python manage.py dbshell
```

If it connects successfully, you'll see:
```
myshp_db=>
```

Type `\q` to exit.

---

## Step 4: Backup SQLite Data (Optional)

If you have important data in SQLite:

```bash
python manage.py dumpdata > backup_data.json
```

---

## Step 5: Delete SQLite Database

**⚠️ Only do this if you're sure you don't need the SQLite data!**

```bash
del db.sqlite3
```

---

## Step 6: Run Migrations

```bash
# Create migrations (if any new changes)
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
  ...
```

---

## Step 7: Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts:
- Username: `admin` (or your choice)
- Email: `admin@edithcloths.com` (or your email)
- Password: [enter a strong password]

---

## Step 8: Test Everything

```bash
# Start development server
python manage.py runserver
```

Then test:
1. **Admin Login**: http://127.0.0.1:8000/edith-admin-login/
2. **API Endpoint**: http://127.0.0.1:8000/api/products/

---

## Troubleshooting

### "could not connect to server"
- Make sure PostgreSQL is running
- Check if PostgreSQL service is started:
  ```bash
  # Windows: Check Services
  services.msc
  # Look for "postgresql-x64-15" or similar
  ```

### "password authentication failed"
- Check your `.env` file has the correct password
- Try using the `postgres` user instead:
  ```
  DATABASE_URL=postgres://postgres:YOUR_PASSWORD@localhost:5432/myshp_db
  ```

### "database does not exist"
- Create the database:
  ```sql
  psql -U postgres
  CREATE DATABASE myshp_db;
  \q
  ```

### "psql: command not found"
- Add PostgreSQL to your PATH, or use full path:
  ```bash
  # Usually located at:
  C:\Program Files\PostgreSQL\15\bin\psql.exe -U postgres
  ```

---

## Quick Commands Reference

```bash
# Connect to PostgreSQL
psql -U postgres

# List databases
\l

# Connect to specific database
\c myshp_db

# List tables
\dt

# Exit
\q
```

---

## ✅ Verification Checklist

- [ ] PostgreSQL is running
- [ ] Database `myshp_db` created
- [ ] `.env` file created with correct `DATABASE_URL`
- [ ] Connection test successful (`python manage.py dbshell`)
- [ ] Migrations run successfully
- [ ] Superuser created
- [ ] Development server starts without errors
- [ ] Admin login works

---

**Need help?** Check `POSTGRESQL_MIGRATION_GUIDE.md` for detailed instructions!










