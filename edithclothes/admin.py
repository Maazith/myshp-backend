"""
Custom Admin Site Configuration
"""
from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import path, reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.template.response import TemplateResponse
from django.middleware.csrf import get_token


class CustomAdminSite(admin.AdminSite):
    """Custom Admin Site with custom login view that always provides form"""
    site_header = "EdithCloths Admin"
    site_title = "EdithCloths Admin"
    index_title = "Welcome to EdithCloths Administration"
    
    def get_urls(self):
        """Override to ensure our custom login view is used"""
        urls = super().get_urls()
        # Insert our custom login before other URLs
        custom_urls = [
            path('login/', self.login, name='login'),
        ]
        return custom_urls + urls
    
    @never_cache
    @csrf_protect
    def login(self, request, extra_context=None):
        """
        Display the login form for the given HttpRequest.
        Always ensures form is available in context.
        """
        from django.contrib.auth import REDIRECT_FIELD_NAME, login
        
        # Get redirect URL
        redirect_to = request.POST.get(REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME, ''))
        
        # If already logged in, redirect
        if request.method == 'GET' and self.has_permission(request):
            try:
                index_path = reverse('admin:index', current_app=self.name)
            except Exception:
                index_path = '/edith-admin-login/'
            return HttpResponseRedirect(index_path)
        
        # Get CSRF token early for fallback
        csrf_token = get_token(request)
        
        # Always create a form - this is the key fix
        try:
            if request.method == 'POST':
                form = AuthenticationForm(request, data=request.POST)
                if form.is_valid():
                    # Log the user in
                    login(request, form.get_user())
                    # Redirect to admin index or next URL
                    if redirect_to:
                        return HttpResponseRedirect(redirect_to)
                    try:
                        index_path = reverse('admin:index', current_app=self.name)
                    except Exception:
                        index_path = '/edith-admin-login/'
                    return HttpResponseRedirect(index_path)
            else:
                # GET request - always create empty form
                form = AuthenticationForm(request)
        except Exception as e:
            # If form creation fails, use fallback HTML immediately
            form = None
        
        # If form is None, use fallback HTML immediately
        if form is None:
            return self._get_fallback_html(csrf_token, redirect_to)
        
        # Build context - ALWAYS include form
        try:
            base_context = self.each_context(request)
        except Exception as e:
            # Fallback if each_context fails
            base_context = {
                'site_header': self.site_header,
                'site_title': self.site_title,
                'site_url': '/',
            }
        
        context = {
            **base_context,
            'title': 'Log in',
            'app_path': request.get_full_path(),
            'username': request.user.get_username() if request.user.is_authenticated else '',
            'form': form,  # ALWAYS include form - this is critical
            REDIRECT_FIELD_NAME: redirect_to,
            'next': redirect_to,
            'site_title': self.site_title,
            'site_header': self.site_header,
        }
        
        if extra_context is not None:
            context.update(extra_context)
        
        request.current_app = self.name
        
        # Use our custom template - this ensures form is always rendered
        try:
            return TemplateResponse(request, 'admin/login.html', context)
        except Exception as e:
            # If template fails, return fallback HTML
            return self._get_fallback_html(csrf_token, redirect_to)
    
    def _get_fallback_html(self, csrf_token, redirect_to):
        """Generate fallback HTML login form"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Log in | {self.site_title}</title>
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
            </style>
        </head>
        <body>
            <div class="login-form">
                <h1>Log in to {self.site_title}</h1>
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
