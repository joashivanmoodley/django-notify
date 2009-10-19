import unittest
from django import http
from django.contrib.messages.middleware import MessagesMiddleware


class MiddlewareTest(unittest.TestCase):
    def setUp(self):
        self.middleware = MessagesMiddleware()

    def test_response_without_messages(self):
        """
        A higher middleware layer may return a request directly before
        messages get applied, so the response middleware is tolerant of
        messages not existing on request.
        """
        request = http.HttpRequest()
        response = http.HttpResponse()
        self.middleware.process_response(request, response)
