#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""doconv

Usage:
  doconv [options] FILE INPUT_FORMAT OUTPUT_FORMAT
  doconv (-h | --help)

Options:
  -o, --output-file=OUTPUT_FILE  Write output of the conversion to OUTPUT_FILE.
  -v, --verbose                  Show additional information.
  -h, --help                     Show this screen.
  --version                      Show version.

"""

from collections import namedtuple
from networkx import nx
from networkx.algorithms.traversal.depth_first_search import dfs_successors
from os import path
from stevedore import extension
import argparse
import logging
import os
import shutil
import sys
# doconv imports
from . import log
from .exceptions import UnsatisfiedDependencyException, FormatException
from .util import append_random_suffix, get_version

global logger
logger = log.setup_custom_logger('root')


class PluginManager(object):

    def __init__(self):
        self.plugins = self.get_available_plugins()
        self.graph = self.create_graph()

    @staticmethod
    def get_available_plugins():
        """Look for all the doconv plugins installed and return only the ones
        having all their dependencies present in the system.
        """

        try:
            mgr = extension.ExtensionManager(
                namespace='doconv.converter',
                invoke_on_load=True,
                propagate_map_exceptions=True,
            )
        except TypeError:
            logger.debug("The installed stevedore version seems to be older than 0.10. This could cause exceptions "
                         "in plugins to be silently ignored.")
            mgr = extension.ExtensionManager(
                namespace='doconv.converter',
                invoke_on_load=True,
            )

        # only plugins whose dependencies are installed will be used
        plugins = []
        for plugin in mgr:
            try:
                plugin.obj.check_dependencies()
                plugins.append(plugin)
                logger.debug("Plugin {0} has been loaded".format(plugin.name))
            except UnsatisfiedDependencyException as e:
                logger.warn(
                    "Plugin {0} could not be loaded because of missing "
                    "dependencies: {1}".format(plugin.name, e))
        return plugins

    def get_plugin(self, name):
        """Returns an instance of the required plugin based on its name.
        Return None if not found.
        """
        plugin_found = None
        for plugin in self.plugins:
            if plugin.name == name:
                plugin_found = plugin.obj
        return plugin_found

    def create_graph(self):
        """Composes the graphs of the different plugins into a single graph.
        """

        # create conversion graph based on loaded plugins
        plugin_graphs = []
        for plugin in self.plugins:
            plugin_graphs.append(plugin.obj.get_supported_conversions_graph())

        joined_graph = nx.MultiDiGraph()
        for graph in plugin_graphs:
            joined_graph.add_edges_from(graph.edges(data=True))
        return joined_graph

    def get_plugin_by_formats(self, input_format, output_format):
        """Return the plugin with highest priority able to convert from
        input_format to output_format.
        """
        available_plugins = self.graph[input_format][output_format]
        plugins_unsorted = [k for k in available_plugins.values()]
        plugins_by_priority = sorted(
            plugins_unsorted, key=lambda k: k['priority'], reverse=True)
        plugin = plugins_by_priority[0]['plugin']
        return plugin


class FormatManager(object):

    def __init__(self):
        plugin_manager = PluginManager()
        self.graph = plugin_manager.graph

    def get_input_formats(self):
        input_formats = []
        for node in self.graph.nodes():
            if len(self.graph.successors(node)) != 0:
                input_formats.append(node)
        return input_formats

    def get_output_formats(self):
        output_formats = []
        for node in self.graph.nodes():
            if len(self.graph.predecessors(node)) != 0:
                output_formats.append(node)
        return output_formats

    def get_output_formats_by_input_format(self, input_format):
        if input_format not in self.graph.nodes():
            raise Exception("Not supported format: {0}".format(input_format))
        # dic whose values are lists
        successors_dic = dfs_successors(self.graph, input_format)
        # convert it to a flatten list
        successors_list = successors_dic.keys(
        ) + [item for sublist in successors_dic.values() for item in sublist]
        # remove formats repeated in the list
        successors_clean_list = list(set(successors_list))
        # the input format can not be an output format of itself
        if successors_clean_list:
            successors_clean_list.remove(input_format)

        return successors_clean_list

    def check_formats(self, input_format, output_format):

        logger.debug("Supported formats: {0}".format(self.graph.nodes()))
        logger.debug(
            "Supported format conversions: {0}".format(self.graph.edges()))

        if input_format not in self.get_input_formats():
            raise FormatException("Not supported input format: {0}".
                                  format(input_format))
        if output_format not in self.get_output_formats():
            raise FormatException("Not supported output format: {0}".
                                  format(output_format))
        if input_format == output_format:
            raise FormatException("Same input and output formats specified")


class Converter(object):

    def __init__(self, input_format, output_format):
        self.input_format = input_format
        self.output_format = output_format
        self.plugin_manager = PluginManager()
        format_manager = FormatManager()
        format_manager.check_formats(self.input_format, self.output_format)

    def execute_plugin_chain(self, input_file, plugin_chain):
        """ Calls each plugin in the needed order feeding as input file
        the output file generated by the plugin previously called.
        """
        files_to_remove = []
        output_file = None

        for plugin_tuple in plugin_chain:
            plugin = self.plugin_manager.get_plugin(plugin_tuple.plugin)

            tmp_output_filename = append_random_suffix(input_file)
            output_file = plugin.convert(input_file, plugin_tuple.input_format,
                                         plugin_tuple.output_format,
                                         tmp_output_filename)

            input_file = output_file
            files_to_remove.append(output_file)
        files_to_remove = files_to_remove[:-1]
        for document in files_to_remove:
            os.remove(document)
        return output_file

    def get_plugin_chain(self):
        """Following the graph_path creates an ordered list of the plugins to
        be called and the input and output format to be used with each plugin.
        """
        plugin_chain = []
        Conversion = namedtuple(
            'conversion', 'plugin input_format output_format')

        conversion_path = self.choose_best_conversion_path()

        for node_pos in range(len(conversion_path) - 1):
            input_format = conversion_path[node_pos]
            output_format = conversion_path[node_pos + 1]
            plugin = self.plugin_manager.get_plugin_by_formats(
                input_format, output_format)
            plugin_chain.extend(
                [Conversion(plugin, input_format, output_format)])

        logger.debug(
            "Plugins used for each transformation: {0}".format(plugin_chain))
        return plugin_chain

    def choose_best_conversion_path(self):
        """Select as path the one that requires less conversions.
        """

        graph = self.plugin_manager.graph
        try:
            conversion_path = nx.shortest_path(
                graph, self.input_format, self.output_format)
        except nx.NetworkXNoPath:
            raise Exception("""
            No combination of plugins available in doconv can convert from
            {0} to {1}""".format(self.input_format, self.output_format))

        conversion_path = conversion_path if graph is not None else None
        logger.debug(
            "Chosen chain of transformations: {0}".format(conversion_path))
        return conversion_path

    def convert(self, input_file, output_file=None):

        plugin_chain = self.get_plugin_chain()
        tmp_output_file = self.execute_plugin_chain(input_file, plugin_chain)

        if output_file is None:
            final_output_file_no_ext = path.splitext(
                path.basename(tmp_output_file))[0]
            output_file = final_output_file_no_ext + '.' + self.output_format
        shutil.move(tmp_output_file, output_file)
        print(
            "Conversion successful: file {0} generated".format(output_file))
        return output_file


def parse_args():
    # top-level parser
    parser = argparse.ArgumentParser()
    parser.version = get_version()
    parser.add_argument('-v', '--verbose', help='show additional information',
                        action='store_true')

    parser.add_argument('--version', action='version')
    subparsers = parser.add_subparsers(help='available doconv commands')

    # convert command
    parser_convert = subparsers.\
        add_parser('convert', help='convert files between different formats')
    parser_convert.set_defaults(func=convert)

    parser_convert.add_argument('-o', '--output_file',
                                help='write output of the conversion to '
                                'OUTPUT_FILE',
                                required=False)

    parser_convert.add_argument('<input_file>',
                                help='input file to be converted')

    parser_convert.add_argument('<input_format>',
                                help='format of <input_file>')

    parser_convert.add_argument('<output_format>',
                                help='format to convert <input_file> to')

    # list command
    parser_list = subparsers.add_parser('list', help='list doconv information')
    subparsers_list = parser_list.add_subparsers()

    parser_list_input_formats = subparsers_list.\
        add_parser('input-formats',
                   help='list the supported input formats')
    parser_list_input_formats.set_defaults(func=list_input_formats)

    parser_list_output_formats = subparsers_list.\
        add_parser('output-formats',
                   help='list the supported output formats')
    parser_list_output_formats.\
        add_argument('-i', '--input_format',
                     help='a document input format. This option restricts the '
                     'listed output formats to the ones that INPUT_FORMAT can '
                     'be converted to',
                     required=False)
    parser_list_output_formats.set_defaults(func=list_output_formats)

    args = parser.parse_args()
    return args


def main():
    # parse CLI arguments
    args_tuple = parse_args()
    args_dic = vars(args_tuple)

    verbose = args_dic['verbose']

    if verbose:
        logger.setLevel(logging.DEBUG)

    try:
        args_tuple.func(args_dic)
    except FormatException as e:
        if not verbose:
            print("Error: {0}".format(e))
        else:
            logger.exception("Error: {0}".format(e))

        print("Please, use doconv list to check the formats supported")
        sys.exit(1)
    except Exception as e:
        if not verbose:
            print("Error: {0}".format(e))
        else:
            logger.exception("Error: {0}".format(e))

        sys.exit(1)


def convert(args):
    input_format = args['<input_format>']
    output_format = args['<output_format>']
    input_file = args['<input_file>']
    output_file = args['output_file']

    converter = Converter(input_format, output_format)
    input_file_path = path.abspath(input_file)

    if output_file:
        output_file_path = path.abspath(output_file)
        converter.convert(input_file_path, output_file_path)
    else:
        converter.convert(input_file_path)


def list_input_formats(args):
    format_manager = FormatManager()
    print("Supported input formats:")
    for input_format in format_manager.get_input_formats():
        print(input_format)


def list_output_formats(args):
    format_manager = FormatManager()
    print("Supported output formats:")
    input_format = args['input_format']
    if not input_format:
        for output_format in format_manager.get_output_formats():
            print(output_format)
    else:
        ofs = format_manager.get_output_formats_by_input_format(input_format)
        for output_format in ofs:
            print(output_format)


if __name__ == '__main__':
    main()
