# ✅ Post-Deployment Verification

After deploying to Render, use this checklist to verify everything is working.

## 🔍 Quick Checks

### 1. Service Status
- [ ] Service shows **"Live"** status in Render Dashboard
- [ ] No error messages in logs
- [ ] Service URL is accessible

### 2. API Endpoints

Test these URLs in your browser:

- [ ] **API Root**: `https://myshp-backend.onrender.com/api/`
  - Should return: `{"message": "EdithCloths Backend API", ...}`

- [ ] **Products**: `https://myshp-backend.onrender.com/api/products/`
  - Should return: `[]` (empty array if no products) or list of products

- [ ] **Categories**: `https://myshp-backend.onrender.com/api/categories/`
  - Should return: `[]` (empty array) or list of categories

- [ ] **Admin**: `https://myshp-backend.onrender.com/admin/`
  - Should show Django admin login page

### 3. Database Connection
- [ ] Service logs show: "✅ Migrations complete!"
- [ ] No database connection errors in logs
- [ ] Admin user can be created

### 4. Frontend Connection
- [ ] Open: `frontend/test-connection.html`
- [ ] Enter backend URL: `https://myshp-backend.onrender.com/api`
- [ ] Click "Test All Connections"
- [ ] All tests show ✅ SUCCESS

## 🧪 Manual Testing

### Test 1: API Root
```bash
curl https://myshp-backend.onrender.com/api/
```

**Expected:** JSON response with API information

### Test 2: Products Endpoint
```bash
curl https://myshp-backend.onrender.com/api/products/
```

**Expected:** JSON array (empty or with products)

### Test 3: Categories Endpoint
```bash
curl https://myshp-backend.onrender.com/api/categories/
```

**Expected:** JSON array (empty or with categories)

## 📋 Environment Variables Check

Verify these are set in Render Dashboard:

- [ ] `DEBUG` = `False`
- [ ] `SECRET_KEY` = (auto-generated)
- [ ] `DATABASE_URL` = (auto-set from database)
- [ ] `DJANGO_SUPERUSER_USERNAME` = (your value)
- [ ] `DJANGO_SUPERUSER_EMAIL` = (your value)
- [ ] `DJANGO_SUPERUSER_PASSWORD` = (your value)

## 🐛 Common Issues

### Issue: 502 Bad Gateway
**Solution:** Service is starting up, wait 1-2 minutes

### Issue: 500 Internal Server Error
**Solution:** Check logs for errors, verify environment variables

### Issue: Database Connection Error
**Solution:** Wait for database to be fully provisioned, check DATABASE_URL

### Issue: CORS Error
**Solution:** Verify frontend URL is in CORS_ALLOWED_ORIGINS

## ✅ Success Criteria

Everything is working when:

1. ✅ Service shows "Live" status
2. ✅ API root returns JSON
3. ✅ All endpoints respond (even if empty)
4. ✅ Frontend can connect
5. ✅ No errors in logs
6. ✅ Admin panel loads

---

**If all checks pass, your backend is fully deployed!** 🎉

