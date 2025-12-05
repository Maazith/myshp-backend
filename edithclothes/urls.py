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
from django.http import JsonResponse
from shop.admin import dashboard_view
from edithclothes.admin import CustomAdminSite

# Create custom admin site instance
admin_site = CustomAdminSite(name='admin')

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

urlpatterns = [
    path('', root_view, name='root'),
    path('edith-admin-login/dashboard/', dashboard_view, name='admin_dashboard'),  # Must come before admin.site.urls
    path('edith-admin-login/', admin_site.urls),  # Use custom admin site
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
