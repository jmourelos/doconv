#!/usr/bin/python

import os
from os import path
import shlex
import subprocess
from lxml import etree


def shell(cmd):
    return subprocess.check_call(shlex.split(cmd))


def shell_output(cmd):
    return subprocess.check_output(shlex.split(cmd))


def joinext(base_filename, extension):
    return '.'.join([base_filename, extension])


def change_ext(filename, extension):
    filename_no_ext = path.splitext(filename)[0]
    return joinext(filename_no_ext, extension)


def xslt_process(input_filename, output_filename, xsl_file):

    xml_input = etree.parse(input_filename)
    xslt_root = etree.parse(xsl_file)
    transform = etree.XSLT(xslt_root)
    transformed_xml = str(transform(xml_input))
    with open(output_filename, 'w') as f:
        f.write(transformed_xml)


    # Two other ways to do it. I let them as documentation. They require some
    # binaries to be available.
    # check_bin_dependency("saxon-xslt")
    # shell("saxon-xslt -o {0} {1} {2}".format(output_filename,
                                             # input_filename, xsl_file))
    # shell("/usr/bin/xsltproc --nonet -o {0} {1} {2}".format(output_filename,
                                                   # xsl_file, input_filename))


def get_xml_namespace(xml_file):
    tree = etree.parse(xml_file)
    ns = tree.getroot().nsmap
    ns_inverted = dict((v, k) for k, v in ns.iteritems())
    return ns_inverted


def which(program):
    """Mimics UNIX which command returning the path to the executable if found
       and None if not found.
    """

    def is_exe(fpath):
        return path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path_dir in os.environ["PATH"].split(os.pathsep):
            path_dir = path_dir.strip('"')
            exe_file = path.join(path_dir, program)
            if is_exe(exe_file):
                return exe_file
    return None


def check_bin_dependency(program):
    """Check that a binary dependency is available in PATH, e.g. git.
    """

    binary = which(program)
    if binary is None:
        raise Exception("""
                        This program requires {0} to be available
                        """.format(program))
    return binary
