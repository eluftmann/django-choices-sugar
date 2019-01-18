#!/usr/bin/env python
# coding=utf-8

import io
import os
from setuptools import find_packages
from setuptools import setup

base_dir = os.path.dirname(os.path.abspath(__file__))

# Load the package's __version__.py module
__version__globals = {}
with open(os.path.join(base_dir, 'choices_sugar', '__version__.py')) as f:
    exec(f.read(), __version__globals)

# Import the README.md and use it as a long description
with io.open(os.path.join(base_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-choices-sugar',
    version=__version__globals['__version__'],
    description='A cleaner approach to declare `choices` for models in Django',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Eryk Luftmann',
    author_email='eluftmann@gmail.com',
    license='MIT',
    url='https://github.com/eluftmann/django-choices-sugar',
    python_requires='==2.7.*',
    packages=find_packages(exclude=('tests',)),
    test_suite='tests',
)
