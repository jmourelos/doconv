from doconv.plugin import base
from networkx import nx
from doconv.util import xslt_process
from os import path


class DocBookToDita(base.PluginBase):

    def __init__(self):
        G = nx.DiGraph()
        G.add_nodes_from(["docbook", "dita"])
        G.add_edges_from([("docbook", "dita")], plugin=__name__.split('.')[-1])
        self.conversions_graph = G

    def check_dependencies(self):
        pass

    def get_supported_conversions_graph(self):
        """Method documentation"""
        return self.conversions_graph

    def convert(self, input_file, input_format, output_format,
                output_file=None):
        print("docbooktodita plugin converting...")
        current_dir = path.dirname(__file__)
        xsl_file = path.join(current_dir, "docbooktodita/db2dita/docbook2dita.xsl")
        xslt_process(input_file, output_file, xsl_file)
        return output_file
