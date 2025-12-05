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

# Simple admin login view
@never_cache
@csrf_protect
def custom_admin_login(request):
    """Simple admin login view that always returns HTML"""
    redirect_to = request.POST.get(REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME, ''))
    csrf_token = get_token(request)
    error_message = ''
    
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
            error_message = 'Please enter a correct username and password. Note that both fields may be case-sensitive.'
    else:
        form = AuthenticationForm(request)
    
    # Return HTML form - simple and clean
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Log in | EdithCloths Admin</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #1a1a1a;
            color: #FFFFFF;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            padding: 2rem;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-container {
            width: 100%;
            max-width: 500px;
            background: rgba(255, 255, 255, 0.05);
            padding: 2.5rem;
            border-radius: 16px;
            border: 1px solid #E6E6E6;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }
        h1 {
            text-align: center;
            margin-bottom: 2rem;
            font-size: 1.75rem;
            font-weight: 600;
        }
        .error {
            color: #FF5252;
            margin-bottom: 1.5rem;
            padding: 0.75rem;
            background: rgba(255, 82, 82, 0.1);
            border-radius: 8px;
            font-size: 0.9rem;
        }
        .form-group {
            margin-bottom: 1.5rem;
        }
        label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 600;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 0.875rem 1rem;
            border-radius: 16px;
            border: 1px solid #E6E6E6;
            background: rgba(255, 255, 255, 0.05);
            color: #FFFFFF;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        input[type="text"]:focus,
        input[type="password"]:focus {
            outline: none;
            border-color: #FFD700;
            background: rgba(255, 255, 255, 0.08);
        }
        button {
            width: 100%;
            padding: 1rem 2rem;
            background: #FFD700;
            color: #000000;
            border: none;
            border-radius: 16px;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        button:hover {
            background: #FFC700;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(255, 215, 0, 0.3);
        }
        button:active {
            transform: translateY(0);
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>Log in to EdithCloths Admin</h1>
        """ + (f'<div class="error">{error_message}</div>' if error_message else '') + """
        <form method="post" action="">
            <input type="hidden" name="csrfmiddlewaretoken" value=""" + csrf_token + """>
            <div class="form-group">
                <label for="id_username">Username</label>
                <input type="text" name="username" id="id_username" required autofocus>
            </div>
            <div class="form-group">
                <label for="id_password">Password</label>
                <input type="password" name="password" id="id_password" required>
            </div>
            <input type="hidden" name="next" value=""" + redirect_to + """>
            <button type="submit">Log in</button>
        </form>
    </div>
</body>
</html>"""
    return HttpResponse(html_content)

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
