from django.shortcuts import redirect
from django.urls import reverse


class RedirectForbiddenToOverleveringMiddleware:
    """Middleware that redirects authenticated users away from 403 pages to Overlevering.

    Behavior:
    - If a view returns a 403 response and the user is authenticated, redirect them to
      the named URL 'overlevering' (path '/overlevering/').
    - Do NOT redirect for API endpoints (paths starting with '/accounts/api/') or
      for XMLHttpRequest/fetch calls (XHR), as those expect JSON responses.
    - Avoid redirect loops by not redirecting when the request is already for Overlevering.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return self.process_response(request, response)

    def process_response(self, request, response):
        try:
            # Only consider real 403 responses
            if response.status_code != 403:
                return response

            # If user not authenticated, keep the 403 (or let login redirect handle it)
            user = getattr(request, 'user', None)
            if not user or not user.is_authenticated:
                return response

            # Avoid redirecting for API endpoints or AJAX/fetch requests
            path = request.path or ''
            if path.startswith('/accounts/api/'):
                return response
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return response

            try:
                over_url = reverse('overlevering')
            except Exception:
                # If for some reason reverse fails, fall back to literal path
                over_url = '/overlevering/'

            # Avoid redirect loops
            if path == over_url:
                return response

            return redirect(over_url)
        except Exception:
            # If anything unexpected happens, return original response
            return response
