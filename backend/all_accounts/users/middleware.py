from django.shortcuts import redirect, render


class LoginRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.path in ['/users/login/', '/']:
            return redirect('dashboard')
        response = self.get_response(request)
        return response


class UnderConstructionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = render(request, "users/under_construction.html")
        return response
