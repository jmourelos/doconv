import abc
from networkx import nx
import inspect
import logging


class PluginBase(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.logger = logging.getLogger('root')

    @abc.abstractmethod
    def get_supported_conversions(self):
        """Return the conversions provided by the plugin implementing this
        method.
        """
        return

    def get_supported_conversions_graph(self):
        # Return a graph representing the format conversions
        # provided by the plugin.

        if not hasattr(self, 'conversions_graph'):
            self.conversions_graph = self._generate_graph()
        return self.conversions_graph

    @abc.abstractmethod
    def convert(self, input_file, output_file, input_format, output_format):
        """Convert a input_file from a specified format to another"""
        return

    @abc.abstractmethod
    def check_dependencies(self):
        """Check that all neccessary dependencies for a particular plugin
        are available in the system, raise an exception otherwise.
        """
        return

    def _get_plugin_priority(self):
        """To be overridden by plugins.
        """
        return 0

    def _generate_graph(self):
        """Generate a directed graph where each node is a document format.
        The representation of a node pointing to another (e.g. from '.doc' to
        '.odt') is called edge and it will contain the name of the plugin being
        able to perform the conversion.
        The graph is the representation of all the format conversions provided
        by this plugin.
        """
        G = nx.MultiDiGraph()
        conversions = self.get_supported_conversions()
        self._add_priority_to_conversions(
            self._get_plugin_priority(), conversions)

        G.add_edges_from(conversions, plugin=self._get_module_name())
        return G

    def _get_nodes_from_edges(self, edges):
        """Convert a list of tuple containing format conversions to
        a list of the formats in the original list.
        """
        nodes = list(set(format for conversion in edges for format in
                         conversion))
        return nodes

    def _add_priority_to_conversions(self, priority, conversions):
        for i, conversion in enumerate(conversions):
            if len(conversion) == 2:
                conversions[i] = conversion + \
                    tuple([dict({"priority": priority})])
        return conversions

    def _get_module_name(self):
        """Get the name of the module containing the class inheriting from this
        class, i.e., the name of the plugin.
        """
        current_class = inspect.getfile(self.__class__)
        current_module = inspect.getmodulename(current_class)
        return current_module
