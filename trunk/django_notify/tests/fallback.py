from django_notify.tests.base import BaseTest
from django_notify.storage.fallback import FallbackStorage


class FallbackTest(BaseTest):
    storage_class = FallbackStorage

    def get_request(self):
        self.session = {}
        request = super(FallbackTest, self).get_request()
        request.session = self.session
        return request

    def check_cookie_store(self, storage, response):
        storage = storage.storages[0]
        # Get a list of cookies, excluding ones with a max-age of 0 (because
        # they have been marked for deletion).
        cookie = response.cookies.get(storage.cookie_name)
        if not cookie:
            return 0
        data = storage._decode(cookie.value)
        if not data:
            return 0
        return len(data)

    def check_session_store(self, storage, response):
        storage = storage.storages[1]
        data = self.session.get(storage.session_key, [])
        return len(data)

    def check_store(self, storage, response):
        return self.check_cookie_store(storage, response) + \
               self.check_session_store(storage, response)

    def test_get(self):
        pass

    def test_no_fallback(self):
        """
        A short number of messages which data size doesn't exceed what is
        allowed in a cookie will all be stored in the CookieBackend.
        
        """
        storage = self.get_storage()
        response = self.get_response()

        for i in range(5):
            storage.add(str(i) * 100)
        storage.update(response)

        cookie_storing = self.check_cookie_store(storage, response)
        self.assertEqual(cookie_storing, 5)
        session_storing = self.check_session_store(storage, response)
        self.assertEqual(session_storing, 0)

    def test_session_fallback(self):
        """
        If the data exceeds what is allowed in a cookie, older messages which
        did not "fit" are stored in the SessionBackend.
        
        """
        storage = self.get_storage()
        response = self.get_response()

        for i in range(5):
            storage.add(str(i) * 900)
        storage.update(response)

        cookie_storing = self.check_cookie_store(storage, response)
        self.assertEqual(cookie_storing, 4)
        session_storing = self.check_session_store(storage, response)
        self.assertEqual(session_storing, 1)
