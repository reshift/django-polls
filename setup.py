# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
 
long_description = open('README.md').read()
 
setup(
    name='django-polls',
    version='0.1',
    description='Polls for django',
    long_description=long_description,
    author='HUB Online',
    author_email='online@hub.nl',
    url='https://github.com/hub-nl/django-polls',
    packages=(
      'polls',
      'polls.migrations',
    ),
    package_data={
      'polls': [
        'templates/polls/*',
      ]
    },
    zip_safe=False,
)