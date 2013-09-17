#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_doconv
----------------------------------

Tests for `doconv` module.
"""

import unittest

from doconv import doconv
from doconv.util import check_bin_dependency, shell
from tempfile import mkdtemp
from os import chdir, path, getcwd
from shutil import rmtree
import inspect

class TestDoconv(unittest.TestCase):
    def get_module_dir(self):
        """Return the absolute path of this module
        __file__ does not work in some cases
        """
        return path.dirname(path.abspath(inspect.stack()[0][1]))
    
    def setUp(self):
        check_bin_dependency("xmllint")

        self.initial_dir = self.get_module_dir()

        self.tmp = mkdtemp()
        chdir(self.tmp)

    def assert_xml(self, xml_file):
        shell("xmllint --noout {0}".format(xml_file))

    def test_convert_asciidoc_docbook(self):
        converter = doconv
        converted_file = converter.convert(path.join(self.initial_dir,
            "samples/asciidoc.txt"), "asciidoc", "docbook", True, path.join(self.tmp, "asciidoc.docbook"))
        self.assert_xml(converted_file)

    def test_convert_docbook_dita(self):
        converter = doconv
        converted_file = converter.convert(path.join(self.initial_dir,
            "samples/docbook.xml"), "docbook", "dita", True, path.join(self.tmp, "docbook.dita"))
        self.assert_xml(converted_file)
        
    def test_convert_asciidoc_dita(self):
        converter = doconv
        converted_file = converter.convert(path.join(self.initial_dir,
            "samples/asciidoc.txt"), "asciidoc", "dita", True, path.join(self.tmp, "asciidoc.dita"))
        self.assert_xml(converted_file)

    def tearDown(self):
        chdir(self.initial_dir)
        rmtree(self.tmp)

if __name__ == '__main__':
    unittest.main()