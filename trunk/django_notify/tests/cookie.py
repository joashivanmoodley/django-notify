from django_notify.tests.base import BaseTest
from django_notify.storage.cookie import CookieStorage


class CookieTest(BaseTest):
    storage_class = CookieStorage

    def check_store(self, storage, response):
        # Get a list of cookies, excluding ones with a max-age of 0 (because
        # they have been marked for deletion).
        cookie = response.cookies.get(storage.cookie_name)
        if not cookie:
            return 0
        data = storage._decode(cookie.value)
        if not data:
            return 0
        return len(data)

    def test_get(self):
        pass

    def test_max_cookie_length(self):
        """
        If the data exceeds what is allowed in a cookie, older messages are
        removed before saving (and returned by the ``update`` method).
        
        """
        storage = self.get_storage()
        response = self.get_response()

        for i in range(5):
            storage.add(str(i) * 900)
        unstored_messages = storage.update(response)

        cookie_storing = self.check_store(storage, response)
        self.assertEqual(cookie_storing, 4)

        self.assertEqual(len(unstored_messages), 1)
        self.assert_(unstored_messages[0].message == '0' * 900)
