# Update Contact Information

## Management Command

A Django management command has been created to update the contact information in SiteSettings.

### Run the Command

```bash
python manage.py update_contact_info
```

This will update:
- **Phone**: `6381902506`
- **Email**: `edith0530s@gmail.com`
- **Address**: `35/1 sivan sannadhi street keeranur (PT) kulathur (TK) Pudukkottai (DT) 622502`
- **WhatsApp**: `6381902506`

### On Render (Production)

If you're deploying on Render, you can run this command via:

1. **Render Shell** (if available on your plan):
   ```bash
   python manage.py update_contact_info
   ```

2. **Via Admin Panel**:
   - Go to Django Admin → Site Settings
   - Update the contact fields manually

3. **Via API** (if you have API access):
   - Use the SiteSettingsUpdateView endpoint

### Manual Update via Admin

1. Go to Django Admin: `https://your-backend-url.onrender.com/admin/`
2. Navigate to **Site Settings**
3. Update:
   - Contact Phone: `6381902506`
   - Contact Email: `edith0530s@gmail.com`
   - Contact Address: `35/1 sivan sannadhi street keeranur (PT) kulathur (TK) Pudukkottai (DT) 622502`
   - WhatsApp Number: `6381902506`
4. Click **Save**

---

**Note**: The frontend will force these correct values even if the API returns old values, but updating the backend ensures consistency across all systems.

