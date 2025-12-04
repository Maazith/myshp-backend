# 🚀 Post-Deployment Steps for Render

## ✅ Your Service is Live!

**Service URL**: `https://myshp-backend.onrender.com`

---

## Step 1: Run Database Migrations

1. In Render Dashboard, go to your service: **myshp-backend**
2. Click **"Shell"** tab (in the left sidebar under MANAGE)
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Wait for it to complete (should see "OK" messages)

---

## Step 2: Create Superuser (Admin Account)

In the same Shell, run:
```bash
python manage.py createsuperuser
```

Enter:
- **Username**: (choose a username, e.g., `admin`)
- **Email**: (your email, e.g., `maazith.md@gmail.com`)
- **Password**: (create a strong password)

---

## Step 3: Test Your API Endpoints

### Test Basic Endpoints:

1. **Products API** (should return products or empty array):
   ```
   https://myshp-backend.onrender.com/api/products/
   ```

2. **Categories API**:
   ```
   https://myshp-backend.onrender.com/api/categories/
   ```

3. **Banners API**:
   ```
   https://myshp-backend.onrender.com/api/banners/
   ```

4. **Admin Panel**:
   ```
   https://myshp-backend.onrender.com/admin/
   ```
   - Login with your superuser credentials

---

## Step 4: Update Frontend to Use Render Backend

Update your frontend API URL to point to Render:

1. Open: `frontend/assets/js/api.js`
2. Find: `const API_BASE = ...`
3. Update to:
   ```javascript
   const API_BASE = "https://myshp-backend.onrender.com";
   ```

---

## Step 5: Test Full Application

1. **Test Frontend**:
   - Open your frontend (local or deployed)
   - Try logging in
   - Browse products
   - Add to cart
   - Checkout

2. **Test Admin**:
   - Login to admin panel
   - Add products
   - View orders

---

## ⚠️ Important Notes

### Free Plan Limitations:
- **Spins down after 15 minutes** of inactivity
- **First request after spin-down**: Takes 30-60 seconds (cold start)
- **Subsequent requests**: Faster (service is warm)

### If Service is Slow:
- This is normal on Free plan
- First request after inactivity will be slow
- Consider upgrading to Standard ($25/month) for production

---

## 🔍 Troubleshooting

### 404 Errors on `/`:
- This is normal - your API is at `/api/`
- Try: `https://myshp-backend.onrender.com/api/products/`

### Database Connection Errors:
- Check `DATABASE_URL` is set in Environment variables
- Verify database is linked to web service

### Static Files Not Loading:
- Static files should work automatically
- Check logs if issues persist

---

## ✅ Verification Checklist

- [ ] Migrations run successfully
- [ ] Superuser created
- [ ] API endpoints respond (check `/api/products/`)
- [ ] Admin panel accessible
- [ ] Frontend updated with new API URL
- [ ] Full application tested

---

**Your backend is deployed! Now test it and update your frontend!** 🎉

