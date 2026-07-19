from django.shortcuts import redirect
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponseForbidden
import re
import logging

logger = logging.getLogger(__name__)

class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'same-origin'
        return response

class SQLInjectionProtectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.blacklist = [
            r"SELECT.*FROM", r"INSERT.*INTO", r"UPDATE.*SET",
            r"DELETE.*FROM", r"DROP.*TABLE", r"UNION.*SELECT",
            r"OR\s+1=\s*1", r"OR\s+true", r"--", r"\;",
        ]
    
    def __call__(self, request):
        if request.method in ['GET', 'POST']:
            data = request.GET if request.method == 'GET' else request.POST
            for key, value in data.items():
                if isinstance(value, str):
                    for pattern in self.blacklist:
                        if re.search(pattern, value, re.IGNORECASE):
                            logger.warning(f"SQL Injection tentée: {value}")
                            return HttpResponseForbidden("Tentative d'injection SQL détectée")
        return self.get_response(request)

class XSSProtectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.xss_patterns = [
            r"<script.*?>.*?</script>", r"javascript:", r"onerror=",
            r"onload=", r"onclick=", r"onmouseover=", r"<iframe",
            r"<embed", r"<object",
        ]
    
    def __call__(self, request):
        if request.method in ['GET', 'POST']:
            data = request.GET if request.method == 'GET' else request.POST
            for key, value in data.items():
                if isinstance(value, str):
                    for pattern in self.xss_patterns:
                        if re.search(pattern, value, re.IGNORECASE):
                            logger.warning(f"XSS tentée: {value}")
                            return HttpResponseForbidden("Tentative d'attaque XSS détectée")
        return self.get_response(request)
