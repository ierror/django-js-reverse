#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os

from setuptools import setup, find_packages


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


setup(
    name='django-js-reverse',
    version='0.10.1a',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Framework :: Django',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
    ],
    license='MIT',
    description='Javascript url handling for Django that doesn\'t hurt.',
    long_description=read('README.rst') + '\n\n' + read('CHANGELOG.rst'),
    author='Bernhard Janetzki',
    author_email='boerni@gmail.com',
    url='https://github.com/ierror/django-js-reverse',
    download_url='http://pypi.python.org/pypi/django-js-reverse/',
    packages=find_packages(),
    package_data={
        'django_js_reverse': [
            'templates/django_js_reverse/*',
        ]
    },
    install_requires=[
        'Django>=1.5',
    ]
)
