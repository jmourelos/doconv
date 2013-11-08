#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requires = [
        'docopt',
        'lxml',
        'networkx',
        'stevedore',
]

version = __import__('doconv').VERSION

setup(
    name='doconv',
    version=version,
    description='conversion from AsciiDoc and DocBook to DITA',
    long_description=readme + '\n\n' + history,
    author='Jacob Mourelos',
    author_email='jacob.mourelos@gmail.com',
    url='https://github.com/jmourelos/doconv',
    packages=[
        'doconv',
        'doconv.plugin',
    ],
    package_dir={'doconv': 'doconv'},
    include_package_data=True,
    install_requires=requires,
    license="BSD",
    zip_safe=False,
    keywords='doconv',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',

    entry_points={
        'console_scripts': [
            'doconv = doconv.doconv:main'
            ],
        'doconv.converter': [
            'asciidoc = doconv.plugin.asciidoc:AsciiDoc',
            'docbooktodita = doconv.plugin.docbooktodita:DocBookToDita',
            ],
        },
)
