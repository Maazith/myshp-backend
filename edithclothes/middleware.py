"""
Custom middleware for error handling
"""
import logging
from django.http import JsonResponse
from django.template import TemplateDoesNotExist
from django.template.response import TemplateResponse

logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware:
    """
    Middleware to catch and log errors, providing better error messages
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except TemplateDoesNotExist as e:
            logger.error(f"Template not found: {e}")
            if request.path.startswith('/admin/'):
                # For admin pages, return a simple error page
                return TemplateResponse(
                    request,
                    'admin/500.html',
                    status=500,
                    context={'error': str(e)}
                )
            return JsonResponse({'error': 'Template not found', 'detail': str(e)}, status=500)
        except Exception as e:
            logger.exception(f"Unhandled exception: {e}")
            if request.path.startswith('/admin/'):
                return TemplateResponse(
                    request,
                    'admin/500.html',
                    status=500,
                    context={'error': str(e) if DEBUG else 'Internal server error'}
                )
            return JsonResponse({'error': 'Internal server error'}, status=500)

