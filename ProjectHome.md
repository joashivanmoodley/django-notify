# Django Notify #

A Django application which provides temporary notifications.

Notification messages persist until a request retrieves them.

As of Django 1.2, temorary notifications are included, and can be found in
`django.contrib.messages`.

## Installation ##

Install from [PYPI](http://pypi.python.org/pypi/django-notify/) (`easy_install django-notify`).

Add the middleware to your `MIDDLEWARE_CLASSES` setting (after `SessionMiddleware`):
```
    'django_notify.middleware.NotificationsMiddleware',
```

Add the context processor into your `TEMPLATE_CONTEXT_PROCESSORS` setting:
```
    'django_notify.context_processors.notifications',
```

## Usage ##

Add a temporary notification message like this:
```
    request.notifications.add('Hello world.')

    # Other methods are provided for adding common message types:
    request.notifications.success('Profile details updated.')
    request.notifications.warning('Your account expires in three days.')
    request.notifications.error('Document deleted.')
```

Use `notifications` in your template:
```
{% if notifications %}
<ul class="notifications">
	{% for message in notifications %}
	<li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
	{% endfor %}
</ul>
{% endif %}
```

## Temporary Storage ##

Django Notify can use different temporary storage backends. To change which storage is being used, add a `NOTIFICATIONS_STORAGE` to your settings, referencing to the module and class of the storage class.

For example, to only store notifications in the session ratehr than using the default cookie/session fallback storage:
```
    NOTIFICATIONS_STORAGE = 'session.SessionStorage'
```

For more info, [read the docs](http://api.rst2a.com/1.0/rst2/html?uri=http://django-notify.googlecode.com/svn/trunk/README&style=lsr).