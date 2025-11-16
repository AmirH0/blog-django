from django.http import HttpResponseForbidden


class BlockIPMiddleware:
    BLOCKED_IPS = ["192.168.1.50" , ""]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")

        if ip in self.BLOCKED_IPS:
            return HttpResponseForbidden("Your IP is blocked!")

        return self.get_response(request)
