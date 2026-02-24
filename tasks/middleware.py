import time
import logging
from django.http import HttpResponseServerError
from django.shortcuts import render

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    """
    Middleware for Logging:
    Logs every request's method, path, and duration.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        
        response = self.get_response(request)
        
        duration = time.time() - start_time
        print(f"[LOG] {request.method} {request.path} - Duration: {duration:.4f}s")
        
        return response

class ErrorHandlingMiddleware:
    """
    Middleware for Error Handling:
    Catches unhandled exceptions and returns a friendly error response.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            logger.error(f"Unhandled exception: {e}")
            # You can return a custom error template here
            return render(request, 'tasks/error.html', {'error': str(e)}, status=500)
        
        return response

class SecurityHeadersMiddleware:
    """
    Middleware for Security:
    Adds custom security headers to every response.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Add basic security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['Referrer-Policy'] = 'no-referrer-when-downgrade'
        
        return response
