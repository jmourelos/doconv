#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_doconv
----------------------------------

Tests for `doconv` module.
"""

import logging
from doconv.exceptions import UnsatisfiedDependencyException
import pytest
from mock import patch
from os import chdir, path
from shutil import rmtree
from tempfile import mkdtemp
# doconv imports
from doconv import doconv
from doconv.doconv import Converter
from doconv.util import append_random_suffix
from tests.util import assert_xml, get_module_dir


def setup_module(module):
    logger = doconv.__dict__['logger']
    logger.setLevel(logging.DEBUG)


def raise_(excp):
    raise excp


class TestConverter():

    NS = "doconv.plugin."
    ASCIIDOC_CHECK = NS + "asciidoc.AsciiDoc.check_dependencies"
    ASCIIDOCTOR_CHECK = NS + "asciidoctor.AsciiDoctor.check_dependencies"

    def setup(self):
        self.initial_dir = get_module_dir()
        self.tmp = mkdtemp()
        chdir(self.tmp)

    def get_sample(self, sample_filename):
        return path.join(self.initial_dir, "samples", sample_filename)

    def generate_output_filename(self):
        return path.join(self.tmp, append_random_suffix())

    def test_convert_asciidoc_docbook(self):
        converter = Converter("asciidoc", "docbook")
        converted_file = converter.convert(self.get_sample("asciidoc.txt"),
                                           self.generate_output_filename())
        assert_xml(converted_file)

    @patch(ASCIIDOC_CHECK, lambda x: raise_(UnsatisfiedDependencyException))
    @patch(ASCIIDOCTOR_CHECK, lambda x: raise_(UnsatisfiedDependencyException))
    def test_convert_asciidoc_docbook__no_plugin_present(self):
        with pytest.raises(Exception):
            Converter("asciidoc", "docbook")

    @patch(ASCIIDOCTOR_CHECK, lambda x: raise_(UnsatisfiedDependencyException))
    def test_convert_asciidoc_docbook__asciidoctor_not_present(self):
        converter = Converter("asciidoc", "docbook")
        converted_file = converter.convert(self.get_sample("asciidoc.txt"),
                                           self.generate_output_filename())
        assert_xml(converted_file)

    @patch(ASCIIDOC_CHECK, lambda x: raise_(UnsatisfiedDependencyException))
    def test_convert_asciidoc_docbook__asciidoc_not_present(self):
        converter = Converter("asciidoc", "docbook")
        converted_file = converter.convert(self.get_sample("asciidoc.txt"),
                                           self.generate_output_filename())
        assert_xml(converted_file)

    def test_convert_docbook_dita(self):
        converter = Converter("docbook", "dita")
        converted_file = converter.convert(self.get_sample("docbook.xml"),
                                           self.generate_output_filename())
        assert_xml(converted_file)

    def test_convert_asciidoc_dita(self):
        converter = Converter("asciidoc", "dita")
        converted_file = converter.convert(self.get_sample("asciidoc.txt"),
                                           self.generate_output_filename())
        assert_xml(converted_file)

    def teardown(self):
        chdir(self.initial_dir)
        rmtree(self.tmp)
