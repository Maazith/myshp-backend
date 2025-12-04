# Admin Panel Dark Theme Guide

## ✅ What Was Updated

### 1. Dark Theme Matching User Theme
- Black background (#000000)
- White text (#FFFFFF)
- Gold accents (#FFD700)
- Light grey borders (#E6E6E6)
- Same font family (Poppins/Inter)

### 2. Mobile Responsive Design
- Responsive dashboard stats grid
- Mobile-friendly tables with horizontal scroll
- Full-width forms on mobile
- Touch-friendly buttons
- Optimized spacing for small screens

### 3. Site Settings in Admin
- Site Settings now properly visible in admin menu
- Organized fieldsets:
  - Basic Information (name, logo, banner, about)
  - Contact Information (email, phone, address, WhatsApp, Instagram)
  - Payment Settings (UPI ID, QR code)
- Auto-redirects to edit form (since it's a singleton)

### 4. Clear All Data Command
- New command: `python manage.py clear_all_data`
- Deletes all demo/test data:
  - Products and Variants
  - Categories
  - Banners
  - Orders and Order Items
  - Carts and Cart Items
  - Payment Proofs
- Preserves:
  - Users
  - Site Settings

---

## 🚀 How to Use

### Clear All Demo Data

```bash
python manage.py clear_all_data
```

Or with force flag (skip confirmation):
```bash
python manage.py clear_all_data --force
```

### Access Site Settings

1. Go to Django Admin: `https://your-backend-url/admin/`
2. Click on **Site Settings** in the menu
3. Update contact information and other settings
4. Click **Save**

### Update Contact Info

```bash
python manage.py update_contact_info
```

---

## 📱 Mobile Responsive Breakpoints

- **768px and below**: Tablet layout
- **480px and below**: Mobile layout

---

## 🎨 Theme Colors

- **Background**: #000000 (Black)
- **Text**: #FFFFFF (White)
- **Accents**: #FFD700 (Gold)
- **Borders**: #E6E6E6 (Light Grey)
- **Hover**: rgba(255, 255, 255, 0.05)

---

## 📝 Files Changed

1. `shop/static/admin/css/custom_admin.css` - Custom dark theme CSS
2. `templates/admin/base_site.html` - Base admin template with theme
3. `templates/admin/dashboard.html` - Dashboard template
4. `shop/admin.py` - Site Settings admin configuration
5. `shop/management/commands/clear_all_data.py` - Clear data command

---

## 🔄 After Deployment

1. **Collect Static Files**:
   ```bash
   python manage.py collectstatic --noinput
   ```

2. **Clear Demo Data** (if needed):
   ```bash
   python manage.py clear_all_data --force
   ```

3. **Update Contact Info**:
   ```bash
   python manage.py update_contact_info
   ```

---

**The admin panel now matches your user theme perfectly!** 🎉

