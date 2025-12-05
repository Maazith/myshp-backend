"""
Custom Admin Site Configuration
"""
from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.template.response import TemplateResponse


class CustomAdminSite(admin.AdminSite):
    """Custom Admin Site with custom login view that always provides form"""
    site_header = "EdithCloths Admin"
    site_title = "EdithCloths Admin"
    index_title = "Welcome to EdithCloths Administration"
    
    @never_cache
    @csrf_protect
    def login(self, request, extra_context=None):
        """
        Display the login form for the given HttpRequest.
        Always ensures form is available in context.
        """
        from django.contrib.auth import REDIRECT_FIELD_NAME, login
        
        redirect_to = request.POST.get(REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME, ''))
        
        # If already logged in, redirect
        if request.method == 'GET' and self.has_permission(request):
            index_path = reverse('admin:index', current_app=self.name)
            return HttpResponseRedirect(index_path)
        
        # Always create a form - this is the key fix
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                # Log the user in
                login(request, form.get_user())
                # Redirect to admin index or next URL
                if redirect_to:
                    return HttpResponseRedirect(redirect_to)
                index_path = reverse('admin:index', current_app=self.name)
                return HttpResponseRedirect(index_path)
        else:
            # GET request - always create empty form
            form = AuthenticationForm(request)
        
        # Build context - ALWAYS include form
        try:
            base_context = self.each_context(request)
        except Exception:
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
        return TemplateResponse(request, 'admin/login.html', context)

