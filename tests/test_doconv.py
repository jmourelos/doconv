#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_doconv
----------------------------------

Tests for `doconv` module.
"""

import unittest

from tempfile import mkdtemp
from os import chdir, path
from shutil import rmtree
import logging
# doconv imports
from doconv import doconv, log
from tests.util import assert_xml, get_module_dir


class TestDoconv(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        log.level = logging.DEBUG
        logger = log.setup_custom_logger('root')
        doconv.__dict__['logger'] = logger

    def setUp(self):
        self.initial_dir = get_module_dir()

        self.tmp = mkdtemp()
        chdir(self.tmp)

    def test_convert_asciidoc_docbook(self):
        converter = doconv
        converted_file = converter.convert(path.join(self.initial_dir,
                                                     "samples/asciidoc.txt"), "asciidoc", "docbook", path.join(self.tmp, "asciidoc.docbook"))
        assert_xml(converted_file)

    def test_convert_docbook_dita(self):
        converter = doconv
        converted_file = converter.convert(path.join(self.initial_dir,
                                                     "samples/docbook.xml"), "docbook", "dita", path.join(self.tmp, "docbook.dita"))
        assert_xml(converted_file)

    def test_convert_asciidoc_dita(self):
        converter = doconv
        converted_file = converter.convert(path.join(self.initial_dir,
                                                     "samples/asciidoc.txt"), "asciidoc", "dita", path.join(self.tmp, "asciidoc.dita"))
        assert_xml(converted_file)

    def tearDown(self):
        chdir(self.initial_dir)
        rmtree(self.tmp)

if __name__ == '__main__':
    unittest.main()
