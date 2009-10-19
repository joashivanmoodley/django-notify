from django.conf import settings
from django.contrib.messages.storage.base import BaseStorage


def get_storage(import_name):
    """
    Import the message storage class described by import_name, where import_name
    is a python path relative to django.contrib.storage.
    """
    bits = import_name.split('.')
    if len(bits) < 2:
        raise TypeError('No class name specified.')
    module_name = '.'.join(bits[:-1])
    class_name = bits[-1]
    try:
        module = __import__('django.contrib.messages.storage.%s' % module_name,
                            globals(), locals(), [class_name])
        storage_class = getattr(module, class_name)
    except (AttributeError, ImportError):
        module = __import__(module_name, globals(), locals(), [class_name])
        storage_class = getattr(module, class_name)
    if not issubclass(storage_class, BaseStorage):
        raise TypeError('Not a messages storage class.')
    return storage_class


Storage = get_storage(getattr(settings, 'MESSAGES_STORAGE',
                              'fallback.FallbackStorage'))
