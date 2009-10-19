from django.conf import settings
from django.contrib.messages.storage import Storage


class MessagesMiddleware(object):
    """
    Middleware which handles temporary messages.
    
    """
    def process_request(self, request):
        request.messages = Storage(request)

    def process_response(self, request, response):
        """
        Update the storage backend (i.e. save the messages).
        
        If not all messages could not be stored and ``DEBUG`` is ``True``, a
        ``ValueError`` will be raised.
        
        """
        # A higher middleware layer may return a request which does not contain
        # messages storage, so make no assumption that it will be there.
        if hasattr(request, 'messages'):
            unstored_messages = request.messages.update(response)
            if unstored_messages and settings.DEBUG:
                raise ValueError('Not all temporary message messages '
                                 'could be stored.')
        return response
