#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `plugin` package.
"""

import pytest
import sys
from tempfile import mkdtemp
from os import chdir, path
from shutil import rmtree
# doconv imports
from doconv.plugin.asciidoc import AsciiDoc
from doconv.plugin.asciidoctor import AsciiDoctor
from doconv.plugin.docbooktodita import DocBookToDita
from doconv import log
import logging
from doconv.util import append_random_suffix
from tests.util import assert_xml, get_module_dir


skipifPy3 = pytest.mark.skipif(sys.version_info >= (3, 0),
                               reason="Python 3 is not supported for \
                                        this plugin.")


def setup_module(module):
    log.level = logging.DEBUG
    log.setup_custom_logger('root')


class TestPlugin():

    def setup(self):
        self.initial_dir = get_module_dir()
        self.tmp = mkdtemp()
        chdir(self.tmp)

    def get_sample(self, sample_filename):
        return path.join(self.initial_dir, "samples", sample_filename)

    def generate_output_filename(self):
        return path.join(self.tmp, append_random_suffix())

    @skipifPy3
    def test_asciidoc_asciidoc_docbook(self):
        converter = AsciiDoc()
        converted_file = converter.convert(self.get_sample("asciidoc.txt"),
                                           "asciidoc", "docbook",
                                           self.generate_output_filename())
        assert_xml(converted_file)

    def test_asciidoctor_asciidoc_docbook(self):
        converter = AsciiDoctor()
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

    def teardown(self):
        chdir(self.initial_dir)
        rmtree(self.tmp)
