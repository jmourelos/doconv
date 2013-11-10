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
from doconv.util import append_random_suffix
from tests.util import assert_xml, get_module_dir


class TestPlugin(unittest.TestCase):

    def setUp(self):
        # TODO. Move logger injection to setUpClass method when dropping python
        # 2.6 support.
        log.level = logging.DEBUG
        log.setup_custom_logger('root')

        self.initial_dir = get_module_dir()

        self.tmp = mkdtemp()
        chdir(self.tmp)

    def get_sample(self, sample_filename):
        return path.join(self.initial_dir, "samples", sample_filename)

    def generate_output_filename(self):
        return path.join(self.tmp, append_random_suffix())

    def test_asciidoc_asciidoc_docbook(self):
        converter = AsciiDoc()
        converted_file = converter.convert(self.get_sample("asciidoc.txt"),
                                           "asciidoc", "docbook",
                                           self.generate_output_filename())
        assert_xml(converted_file)

    def test_docbooktodita_docbook_dita(self):
        converter = DocBookToDita()
        converted_file = converter.convert(self.get_sample("docbook.xml"),
                                           "docbook", "dita",
                                           self.generate_output_filename())
        assert_xml(converted_file)

    def tearDown(self):
        chdir(self.initial_dir)
        rmtree(self.tmp)

if __name__ == '__main__':
    unittest.main()
