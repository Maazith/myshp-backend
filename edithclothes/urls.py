"""
URL configuration for edithclothes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import get_token
from django.http import HttpResponseRedirect
from django.urls import reverse
from shop.admin import dashboard_view

# Use default admin site
admin.site.site_header = "EdithCloths Admin"
admin.site.site_title = "EdithCloths Admin"
admin.site.index_title = "Welcome to EdithCloths Administration"

# Register all models with the custom admin site (with error handling)
try:
    from shop.admin import (
        ProductAdmin, CategoryAdmin, SiteSettingsAdmin, CartAdmin, OrderAdmin,
        ProductVariantInline, CartItemInline, OrderItemInline
    )
    from shop.models import (
        Product, Category, SiteSettings, Cart, Order, ProductVariant,
        ProductImage, Banner, OrderItem, PaymentProof
    )
    
    # Register models with custom admin site
    admin_site.register(Product, ProductAdmin)
    admin_site.register(Category, CategoryAdmin)
    admin_site.register(SiteSettings, SiteSettingsAdmin)
    admin_site.register(Cart, CartAdmin)
    admin_site.register(Order, OrderAdmin)
    admin_site.register(ProductVariant)
    admin_site.register(ProductImage)
    admin_site.register(Banner)
    admin_site.register(OrderItem)
    admin_site.register(PaymentProof)
except Exception as e:
    # If model registration fails, log but don't crash
    import logging
    logger = logging.getLogger(__name__)
    logger.warning(f"Failed to register some models with admin site: {e}")

def root_view(request):
    """Root URL handler - provides API information"""
    return JsonResponse({
        'message': 'EdithCloths Backend API',
        'version': '1.0',
        'endpoints': {
            'admin': '/edith-admin-login/',
            'admin_dashboard': '/edith-admin-login/dashboard/',
            'api': '/api/',
            'api_root': '/api/',
            'api_products': '/api/products/',
        },
        'status': 'online'
    })

# Custom login view that always works
@never_cache
@csrf_protect
def custom_admin_login(request):
    """Simple admin login view that always returns HTML"""
    redirect_to = request.POST.get(REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME, ''))
    csrf_token = get_token(request)
    
    # If already logged in, redirect
    if request.method == 'GET' and request.user.is_authenticated and request.user.is_staff:
        return HttpResponseRedirect('/edith-admin-login/')
    
    # Handle POST
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if redirect_to:
                return HttpResponseRedirect(redirect_to)
            return HttpResponseRedirect('/edith-admin-login/')
    else:
        form = AuthenticationForm(request)
    
    # Always return HTML form
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Log in | EdithCloths Admin</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ background: #1a1a1a; color: #FFFFFF; font-family: Arial, sans-serif; padding: 2rem; margin: 0; }}
            .login-form {{ max-width: 500px; margin: 2rem auto; background: rgba(255,255,255,0.05); padding: 2.5rem; border-radius: 16px; border: 1px solid #E6E6E6; }}
            h1 {{ margin-top: 0; text-align: center; }}
            label {{ display: block; margin-bottom: 0.5rem; font-weight: 600; }}
            input[type="text"], input[type="password"] {{ width: 100%; box-sizing: border-box; padding: 0.875rem 1rem; margin-bottom: 1.5rem; border-radius: 16px; border: 1px solid #E6E6E6; background: rgba(255,255,255,0.05); color: #FFFFFF; font-size: 1rem; }}
            button {{ width: 100%; padding: 1rem 2rem; background: #FFD700; color: #000; border: none; border-radius: 16px; font-weight: 600; cursor: pointer; font-size: 1rem; }}
            button:hover {{ opacity: 0.9; }}
            .error {{ color: #FF5252; margin-bottom: 1rem; }}
        </style>
    </head>
    <body>
        <div class="login-form">
            <h1>Log in to EdithCloths Admin</h1>
            {f'<div class="error">Please enter a correct username and password.</div>' if form.errors else ''}
            <form method="post" action="">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                <div>
                    <label for="id_username">Username:</label>
                    <input type="text" name="username" id="id_username" required autofocus>
                </div>
                <div>
                    <label for="id_password">Password:</label>
                    <input type="password" name="password" id="id_password" required>
                </div>
                <input type="hidden" name="next" value="{redirect_to}">
                <button type="submit">Log in</button>
            </form>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

urlpatterns = [
    path('', root_view, name='root'),
    path('edith-admin-login/dashboard/', dashboard_view, name='admin_dashboard'),
    path('edith-admin-login/login/', custom_admin_login, name='admin_login'),
    path('edith-admin-login/', admin.site.urls),  # Use default admin site
    path('api/', include('shop.urls')),
]

# Serve media files in production (Render handles static files via WhiteNoise)
# Media files need to be served separately
from django.views.static import serve
from django.urls import re_path
import os

# Serve media files in both development and production
# Only serve if MEDIA_ROOT exists and is accessible
try:
    if settings.MEDIA_ROOT and os.path.exists(settings.MEDIA_ROOT):
        urlpatterns += [
            re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        ]
except Exception:
    # If media root doesn't exist or can't be accessed, skip media serving
    # This prevents 500 errors on first deployment
    pass

# Only serve static files in development (WhiteNoise handles in production)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
