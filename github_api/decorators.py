from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

def csrf_exempt_middleware(get_response):
    def middleware(request):
        setattr(request, '_dont_enforce_csrf_checks', True)
        response = get_response(request)
        return response
    return middleware