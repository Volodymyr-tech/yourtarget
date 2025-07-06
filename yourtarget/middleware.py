from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest


class MyMiddleWare(SessionMiddleware):
        def process_request(self, request: HttpRequest):
            cookies = request.COOKIES.get('sessionid')
            request.sessionid = cookies