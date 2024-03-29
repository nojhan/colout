#!/usr/bin/env python3

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py bdist_wheel --universal upload')
    sys.exit()

packages = ['colout']

requires = ['pygments', 'babel']

setup_requires = ['setuptools_scm']

classifiers = """
Environment :: Console
Development Status :: 5 - Production/Stable
License :: OSI Approved :: GNU General Public License v3 (GPLv3)
Operating System :: POSIX
Operating System :: POSIX :: Linux
Programming Language :: Python :: 3
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Topic :: Utilities
Topic :: Text Processing
Topic :: Text Processing :: Filters
""".strip().split('\n')

setup(
    name='colout',
    use_scm_version=True,
    classifiers=classifiers,
    description='Color Up Arbitrary Command Output.',
    entry_points={
        'console_scripts': ['colout=colout.colout:main'],
    },
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    long_description_content_type='text/markdown;variant=CommonMark',
    author='nojhan',
    author_email='nojhan@nojhan.net',
    url='http://nojhan.github.com/colout/',
    packages=packages,
    package_data={'': ['LICENSE', 'README.md']},
    package_dir={'colout': 'colout'},
    python_requires='>=3.5',
    setup_requires=setup_requires,
    include_package_data=True,
    install_requires=requires,
    license='GPLv3',
    zip_safe=False,
)
