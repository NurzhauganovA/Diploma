from django.http import HttpRequest
from django.shortcuts import redirect


class AuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        response = self.get_response(request)

        if not request.user.is_authenticated:
            if "/admin" not in (path := request.path) and "/auth" not in path:
                return redirect("login")

        return response
