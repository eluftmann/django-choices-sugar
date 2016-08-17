#!/usr/bin/env python
# coding=utf-8

from setuptools import setup

from choices_sugar import __version__


setup(
    name='django-choices-sugar',
    version=__version__,
    description='A cleaner and more compact way to declare "choices" in Django',
    url='https://github.com/eluftmann/django-choices-sugar',
    author='Eryk Luftmann',
    author_email='eluftmann@gmail.com',
    py_modules=['choices_sugar'],
)
