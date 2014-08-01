# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
 
long_description = open('README.md').read()
 
setup(
    name='django-polls',
    version='0.1.5',
    description='Polls for django',
    long_description=long_description,
    author='Reshift Digital',
    author_email='ot@reshift.nl',
    url='https://github.com/reshift/django-polls',
    packages=(
      'polls',
      'polls.migrations',
      'polls.templatetags',
    ),
    package_data={
      'polls': [
        'templates/polls/*',
      ]
    },
    zip_safe=False,
)
