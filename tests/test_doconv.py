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
from doconv.util import append_random_suffix
from tests.util import assert_xml, get_module_dir


class TestDoconv(unittest.TestCase):

    def setUp(self):
        # TODO. Move logger injection to setUpClass method when dropping python
        # 2.6 support.
        log.level = logging.DEBUG
        logger = log.setup_custom_logger('root')
        doconv.__dict__['logger'] = logger

        self.initial_dir = get_module_dir()

        self.tmp = mkdtemp()
        chdir(self.tmp)

    def get_sample(self, sample_filename):
        return path.join(self.initial_dir, "samples", sample_filename)

    def generate_output_filename(self):
        return path.join(self.tmp, append_random_suffix())

    def test_convert_asciidoc_docbook(self):
        converter = doconv
        converted_file = converter.convert(self.get_sample("asciidoc.txt"),
                                           "asciidoc", "docbook",
                                           self.generate_output_filename())
        assert_xml(converted_file)

    def test_convert_docbook_dita(self):
        converter = doconv
        converted_file = converter.convert(self.get_sample("docbook.xml"),
                                           "docbook", "dita",
                                           self.generate_output_filename())
        assert_xml(converted_file)

    def test_convert_asciidoc_dita(self):
        converter = doconv
        converted_file = converter.convert(self.get_sample("asciidoc.txt"),
                                           "asciidoc", "dita",
                                           self.generate_output_filename())
        assert_xml(converted_file)

    def tearDown(self):
        chdir(self.initial_dir)
        rmtree(self.tmp)

if __name__ == '__main__':
    unittest.main()
