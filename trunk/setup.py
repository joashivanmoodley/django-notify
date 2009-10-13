#!/usr/bin/env python
from distutils.core import setup


README_FILE = open('README')
try:
    long_description = README_FILE.read()
finally:
    README_FILE.close()


setup(
    name='django-notify',
    version='1.1.0',
    packages=[
        'django_notify',
        'django_notify.storage',
        'django_notify.tests'
    ],
    author='Chris Beaven',
    author_email='smileychris@gmail.com',
    description='A Django application which provides temporary notifications.',
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    platforms=['any'],
    url='http://code.google.com/p/django-notify/',
    download_url='http://code.google.com/p/django-notify/source/checkout',
)
