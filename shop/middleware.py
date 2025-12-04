from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import logout

EXEMPT_PATHS = [
    '/admin/',
    '/api/auth/login',
    '/api/auth/register',
    '/api/auth/refresh',
    '/api/products/',
    '/api/categories/',
    '/api/banners/',
    '/media/',
    '/static/',
]


class LoginFirstMiddleware:
    """Redirect to login page if user is not authenticated"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if path should be exempt
        path = request.path
        
        # Allow admin and API endpoints
        if any(path.startswith(exempt) for exempt in EXEMPT_PATHS):
            return self.get_response(request)
        
        # Allow frontend static files
        if path.startswith('/static/') or path.startswith('/media/'):
            return self.get_response(request)
        
        # If not authenticated and not exempt, redirect to login
        if not request.user.is_authenticated:
            # Only redirect frontend pages, not API calls
            if not path.startswith('/api/'):
                login_url = reverse('frontend:login') if hasattr(reverse, 'frontend:login') else '/pages/login.html'
                return redirect(login_url)
        
        return self.get_response(request)

