from django_notify.storage.base import BaseStorage
from django_notify.storage.cookie import CookieStorage
from django_notify.storage.session import SessionStorage


class FallbackStorage(BaseStorage):
    """
    A combination storage backend which tries to store all messages in the
    first backend, storing any unstored messages in each subsequent backend.
    backend.
     
    """
    storage_classes = (CookieStorage, SessionStorage)

    def __init__(self, *args, **kwargs):
        super(FallbackStorage, self).__init__(*args, **kwargs)
        self.storages = [storage_class(*args, **kwargs)
                         for storage_class in self.storage_classes]

    def _get(self):
        """
        Get a single list of messages from all storage backends.
        
        """
        result = []
        for storage in self.storages:
            result.extend(storage._get() or [])
        return result

    def _store(self, messages, response):
        """
        Store the messages, returning any unstored messages after trying all
        backends.
        
        For each storage backend, any messages not stored are passed on to the
        next backend.
        
        """
        for storage in self.storages:
            messages = storage._store(messages, response)
        return messages
