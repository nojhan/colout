#!/usr/bin/env python3

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python3 setup.py sdist upload')
    sys.exit()

packages = ['colout']

requires = ['argparse; python_version < "2.7"', 'pygments', 'babel']

setup_requires = ['setuptools_scm']

setup(
    name='colout',
    use_scm_version=True,
    description='Color Up Arbitrary Command Output.',
    long_description=open('README.md').read(),
    author='nojhan',
    author_email='nojhan@nojhan.net',
    url='http://nojhan.github.com/colout/',
    packages=packages,
    package_data={'': ['LICENSE', 'README.md']},
    package_dir={'colout': 'colout'},
    scripts=['bin/colout'],
    setup_requires=setup_requires,
    include_package_data=True,
    install_requires=requires,
    license='GPLv3',
    zip_safe=False,
)
