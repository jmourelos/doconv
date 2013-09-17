from doconv.plugin import base
from networkx import nx
from doconv.util import shell, check_bin_dependency 


class AsciiDoc(base.PluginBase):

    def __init__(self):
        G = nx.DiGraph()
        G.add_nodes_from(["asciidoc", "docbook"])
        G.add_edges_from([("asciidoc", "docbook")],
                         plugin=__name__.split('.')[-1])
        self.conversions_graph = G

    def check_dependencies(self):
        check_bin_dependency("asciidoc")

    def get_supported_conversions_graph(self):
        """Method documentation"""
        return self.conversions_graph

    def convert(self, input_file, input_format, output_format,
                output_file=None):
        print("Asciidoc plugin converting...")
        shell("asciidoc -b docbook -o {0} {1}".format(output_file, input_file))
        return output_file
