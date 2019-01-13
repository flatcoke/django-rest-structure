import re

from rest_framework import status


class Response403To401Middleware:
    """
    Rest Framework 을 위한 전용 커스텀 미들웨어에 대해 response format 을 자동으로 세팅
    """
    METHOD = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTION')

    def __init__(self, get_response):
        self.get_response = get_response
        self.API_URLS = [
            re.compile(r'^(.*)/api'),
            re.compile(r'^api'),
        ]

    def __call__(self, request):
        response = None
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

    def process_response(self, request, response):
        """
        If not is_authenticated and status code is 403
        It makes it to be 401 because client side needs it for
        redirect to login page
        """
        path = request.path_info.lstrip('/')
        valid_urls = (url.match(path) for url in self.API_URLS)

        if request.method not in self.METHOD or not any(valid_urls):
            return response
        request.user.is_authenticated

        if request.user.is_anonymous and \
                response.status_code == status.HTTP_403_FORBIDDEN:
            response.status_code = status.HTTP_401_UNAUTHORIZED
        return response
