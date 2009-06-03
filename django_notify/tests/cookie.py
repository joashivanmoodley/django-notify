from django_notify.tests.base import BaseTest
from django_notify.storage.cookie import CookieStorage


class CookieTest(BaseTest):
    storage_class = CookieStorage

    def check_store(self, storage, response):
        pass

    def test_get(self):
        pass
