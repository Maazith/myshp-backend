"""
URL configuration for edithclothes project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from shop.admin import dashboard_view
from shop import views

# Use default admin site - models are already registered in shop/admin.py
admin.site.site_header = "EdithCloths Admin"
admin.site.site_title = "EdithCloths Admin"
admin.site.index_title = "Welcome to EdithCloths Administration"

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
    path('edith-admin-login/dashboard/', dashboard_view, name='admin_dashboard'),
    path('edith-admin-login/', admin.site.urls),  # Use default Django admin
    path('api/', include('shop.urls')),
    # User authentication URLs
    path('login/', views.user_login_view, name='user_login'),
    path('signup/', views.user_signup_view, name='user_signup'),
    path('logout/', views.user_logout_view, name='user_logout'),
]

# Serve media files in production (Render handles static files via WhiteNoise)
from django.views.static import serve
from django.urls import re_path
import os

# Serve media files in both development and production
try:
    if settings.MEDIA_ROOT and os.path.exists(settings.MEDIA_ROOT):
        urlpatterns += [
            re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        ]
except Exception:
    pass

# Only serve static files in development (WhiteNoise handles in production)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
