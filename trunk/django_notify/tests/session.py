from django_notify.tests.base import BaseTest
from django_notify.storage.session import SessionStorage


class SessionTest(BaseTest):
    storage_class = SessionStorage

    def get_request(self):
        request = super(SessionTest, self).get_request()
        request.session = {}
        return request

    def check_store(self, storage, response):
        pass

    def test_get(self):
        pass
