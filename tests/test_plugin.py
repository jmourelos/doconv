#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `plugin` package.
"""

import unittest

from doconv.plugin.asciidoc import AsciiDoc
from doconv.util import check_bin_dependency, shell
from tempfile import mkdtemp
from os import chdir, path, getcwd
from shutil import rmtree

class TestAsciiDoc(unittest.TestCase):

    def setUp(self):
        check_bin_dependency("xmllint")

        self.initial_dir = getcwd()

        self.tmp = mkdtemp()
        chdir(self.tmp)
    
    def assert_xml(self, xml_file):
        shell("xmllint --noout {0}".format(xml_file))

    def test_asciidoc_asciidoc_docbook(self):
        converter = AsciiDoc()
        converted_file = converter.convert(path.join(self.initial_dir,
            "samples/asciidoc.txt"), "asciidoc", "docbook", path.join(self.tmp, "asciidoc.docbook"))
        self.assert_xml(converted_file)

    def test_docbooktodita_docbook_dita(self):
        converter = AsciiDoc()
        converted_file = converter.convert(path.join(self.initial_dir,
            "samples/docbook.xml"), "docbook", "dita", path.join(self.tmp, "docbook.dita"))
        self.assert_xml(converted_file)

    def tearDown(self):
        chdir(self.initial_dir)
        rmtree(self.tmp)

if __name__ == '__main__':
    unittest.main()
