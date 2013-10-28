#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `plugin` package.
"""

import unittest
from tempfile import mkdtemp
from os import chdir, path
from shutil import rmtree
# doconv imports
from doconv.plugin.asciidoc import AsciiDoc
from doconv.plugin.docbooktodita import DocBookToDita
from doconv import log
import logging
from tests.util import assert_xml, get_module_dir


class TestPlugin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        log.level = logging.DEBUG
        log.setup_custom_logger('root')

    def setUp(self):
        self.initial_dir = get_module_dir()

        self.tmp = mkdtemp()
        chdir(self.tmp)

    def test_asciidoc_asciidoc_docbook(self):
        converter = AsciiDoc()
        converted_file = converter.convert(path.join(self.initial_dir,
                                                     "samples/asciidoc.txt"), "asciidoc", "docbook", path.join(self.tmp, "asciidoc.docbook"))
        assert_xml(converted_file)

    def test_docbooktodita_docbook_dita(self):
        converter = DocBookToDita()
        converted_file = converter.convert(path.join(self.initial_dir,
                                                     "samples/docbook.xml"), "docbook", "dita", path.join(self.tmp, "docbook.dita"))
        assert_xml(converted_file)

    def tearDown(self):
        chdir(self.initial_dir)
        rmtree(self.tmp)

if __name__ == '__main__':
    unittest.main()
