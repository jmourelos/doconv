#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
    from setuptools.command.test import test as TestCommand
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requires = [
        'lxml',
        'networkx',
        'stevedore',
]

version = __import__('doconv').VERSION

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests']
        self.test_suite = True
    def run_tests(self):
    #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=['pytest'],
    cmdclass = {'test': PyTest},

    entry_points={
        'console_scripts': [
            'doconv = doconv.doconv:main',
            ],
        'doconv.converter': [
            'asciidoc = doconv.plugin.asciidoc:AsciiDoc',
            'asciidoctor = doconv.plugin.asciidoctor:AsciiDoctor',
            'docbooktodita = doconv.plugin.docbooktodita:DocBookToDita',
            ],
        },
)
