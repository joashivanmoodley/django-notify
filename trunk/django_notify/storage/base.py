'''
Base temporary notification storage.

This is not a complete class, to be usable it should be subclassed and the
appropriate methods overridden.
'''

from django.utils.encoding import force_unicode


class Notification(object):
    def __init__(self, message, tags='', extras=None):
        self.message = message
        self.tags = tags
        self.extras = extras or {}

    def __unicode__(self):
        return force_unicode(self.message)


class BaseStorage(object):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.new_data = []
        self.used = False
        self.added_new = False
        super(BaseStorage, self).__init__(*args, **kwargs)

    def __len__(self):
        return len(self.data) + len(self.new_data)

    def __iter__(self):
        self.used = True
        if self.new_data:
            self.data.extend(self.new_data)
            self.new_data = []
        return iter(self.data)

    def __contains__(self, item):
        return item in self._data

    @property
    def data(self):
        if not hasattr(self, '_data'):
            self._data = self.get() or []
        return self._data

    def get(self):
        raise NotImplementedError()

    def store(self, data, response):
        raise NotImplementedError()

    def update(self, response):
        if self.used:
            self.store(self.new_data, response)
        if self.added_new:
            data = self.data + self.new_data
            self.store(data, response)

    def add(self, message, tags='', **extras):
        if not message:
            return
        self.added_new = True
        notification = Notification(message, tags, extras)
        self.data.append(notification)
