#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Some convenient functions for testing.
"""

from doconv.util import check_bin_dependency, shell
from os import path
import inspect


def get_module_dir():
    """Return the absolute path of this module
     __file__ does not work in some cases
    """
    return path.dirname(path.abspath(inspect.stack()[0][1]))


def assert_xml(xml_file):
    """Validate a XML file
    """
    check_bin_dependency("xmllint")
    shell("xmllint --noout {0}".format(xml_file))
