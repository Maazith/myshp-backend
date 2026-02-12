# Create .env File Manually

Since `.env` files are gitignored (for security), you need to create it manually.

## Quick Method

**Copy and paste this into a new file named `.env` in `backend/backend/backend/`:**

```env
# Django Environment Variables for Local Development
# IMPORTANT: This file is for local development only
# Never commit this file to git (it's in .gitignore)

# Database Configuration
# Using default PostgreSQL user 'postgres'
DATABASE_URL=postgres://postgres:maazith2005@localhost:5432/myshp_db

# Django Secret Key (for local development only)
SECRET_KEY=django-insecure-change-this-in-production

# Debug Mode (True for development)
DEBUG=True
```

## Steps:

1. **Navigate to:** `backend\backend\backend\`
2. **Create new file:** `.env` (no extension, just `.env`)
3. **Paste the content above**
4. **Save the file**

## Verify it was created:

```bash
cd backend\backend\backend
dir .env
```

You should see `.env` listed.

## Next Steps:

After creating `.env`, proceed with:
1. Create PostgreSQL database: `CREATE DATABASE myshp_db;`
2. Test connection: `python manage.py dbshell`
3. Run migrations: `python manage.py migrate`










