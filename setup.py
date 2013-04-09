#!/usr/bin/env python

import os
import sys

import colout

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = ['colout']

requires = []

setup(
    name='colout',
    version='0.1',
    description='Color Up Arbitrary Command Ouput.',
    long_description=open('README.md').read(),
    author='nojhan',
    author_email='nojhan@nojhan.net',
    url='http://nojhan.github.com/colout/',
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'colout': 'colout'},
    include_package_data=True,
    install_requires=requires,
    license=open('LICENSE').read(),
    zip_safe=False,
)
