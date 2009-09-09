import pickle
from hashlib import sha1
from django.conf import settings
from django_notify.storage.base import BaseStorage


class CookieStorage(BaseStorage):
    """
    Cookie based temporary notification storage backend.
    
    """
    cookie_name = 'notifications'
    max_cookie_size = 4096

    def _get(self):
        """
        Retrieve a list of messages from the notifications cookie.
        
        """
        data = self.request.COOKIES.get(self.cookie_name)
        return self._decode(data)

    def _update_cookie(self, encoded_data, response):
        """
        Either set the cookie with the encoded data if there is any data to
        store, otherwise delete the cookie.
        
        """
        if encoded_data:
            response.set_cookie(self.cookie_name, encoded_data)
        else:
            response.delete_cookie(self.cookie_name)
        
    def _store(self, messages, response):
        """
        Store the messages to a cookie, returning a list of any messages which
        could not be stored.
        
        If the encoded data is larger than ``max_cookie_size``, remove the
        oldest messages until the data fits (these are the messages which are
        returned).
        
        """
        unstored_messages = []
        encoded_data = self._encode(messages)
        if self.max_cookie_size:
            while encoded_data and len(encoded_data) > self.max_cookie_size:
                unstored_messages.append(messages.pop(0))
                encoded_data = self._encode(messages)
        self._update_cookie(encoded_data, response)
        return unstored_messages

    def _hash(self, value):
        """
        Create a SHA1 hash based on the value combined with the project
        setting's SECRET_KEY.
        
        """
        return sha1(value + settings.SECRET_KEY).hexdigest()

    def _encode(self, messages):
        """
        Return an encoded version of the messages list which can be stored as
        plain text.
        
        Since the data will be retrieved from the client-side, the encoded data
        also contains a hash to ensure that the data was not tampered with.
        
        """
        if messages:
            value = pickle.dumps(messages, pickle.HIGHEST_PROTOCOL)
            return '%s$%s' % (self._hash(value), value)

    def _decode(self, data):
        """
        Safely decode a encoded text stream back into a list of messages.
        
        If the encoded text stream contained an invalid hash or was in an
        invalid format, ``None`` is returned.
        
        """
        if not data:
            return None
        bits = data.split('$', 1)
        if len(bits) == 2:
            hash, value = bits
            if hash == self._hash(value):
                try:
                    # If we get here (and the pickle works), everything is
                    # good. In any other case, drop back and return None.
                    return pickle.loads(value)
                except:
                    pass
        # Mark the data as used (so it gets removed) since something was wrong
        # with the data.
        self.used = True
        return None
