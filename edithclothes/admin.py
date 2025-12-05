"""
Custom Admin Site Configuration
"""
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.template.response import TemplateResponse
from django.urls import path, reverse_lazy
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect


class CustomAdminSite(admin.AdminSite):
    """Custom Admin Site with custom login view"""
    site_header = "EdithCloths Admin"
    site_title = "EdithCloths Admin"
    index_title = "Welcome to EdithCloths Administration"
    
    def get_urls(self):
        """Override to add custom login view"""
        urls = super().get_urls()
        # Add custom login before default admin URLs
        custom_urls = [
            path('login/', self.admin_view(self.login), name='login'),
        ]
        return custom_urls + urls
    
    @never_cache
    def login(self, request, extra_context=None):
        """
        Display the login form for the given HttpRequest.
        """
        if request.method == 'GET' and self.has_permission(request):
            # Already logged in, redirect to admin index
            index_path = reverse_lazy('admin:index', current_app=self.name)
            return HttpResponseRedirect(index_path)
        
        from django.contrib.auth.forms import AuthenticationForm
        from django.contrib.auth import REDIRECT_FIELD_NAME
        from django.urls import reverse
        from django.http import HttpResponseRedirect
        
        context = {
            **self.each_context(request),
            'title': 'Log in',
            'app_path': request.get_full_path(),
            'username': request.user.get_username(),
        }
        
        # Always provide a form, even if empty
        if request.method == 'GET':
            form = AuthenticationForm(request)
        else:
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                from django.contrib.auth import login
                login(request, form.get_user())
                return HttpResponseRedirect(self.get_login_redirect_url(request))
        
        context['form'] = form
        context[REDIRECT_FIELD_NAME] = request.GET.get(REDIRECT_FIELD_NAME, '')
        
        if extra_context is not None:
            context.update(extra_context)
        
        defaults = {
            'extra_context': context,
            'current_app': self.name,
            'authentication_form': form,
            'template_name': 'admin/login.html',
        }
        request.current_app = self.name
        
        return auth_views.LoginView.as_view(**defaults)(request)

