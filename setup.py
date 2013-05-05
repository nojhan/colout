#!/usr/bin/env python3

import os
import sys

#import colout

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python3 setup.py sdist upload')
    sys.exit()

packages = ['colout']

requires = ['argparse', 'pygments', 'babel']

classifiers = """\
Development Status :: 4 - Beta
Environment :: Console
Intended Audience :: End Users/Desktop
License :: OSI Approved :: GNU General Public License v3 (GPLv3)
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 2.5
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Topic :: Text Processing
Topic :: Utilities
Topic :: Software Development :: Libraries :: Python Modules
"""

setup(
    name='colout',
    version='0.1',
    description='Color Up Arbitrary Command Ouput.',
    long_description=open('README').read(),
    author='nojhan',
    author_email='nojhan@nojhan.net',
    url='http://nojhan.github.com/colout/',
    download_url = 'https://pypi.python.org/packages/source/C/colout/colout-0.1.tar.gz',
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'colout': 'colout'},
    scripts=['bin/colout'],
    include_package_data=True,
    install_requires=requires,
    license=open('LICENSE').read(),
    classifiers = filter(None, classifiers.split("\n")),
    zip_safe=False,
)
