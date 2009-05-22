'''
Middleware which handles temporary notifications.
'''

from django_notify.storage import Storage


class NotificationsMiddleware(object):
    def process_request(self, request):
        request.notifications = Storage(request)

    def process_response(self, request, response):
        request.notifications.update(response)
        return response
