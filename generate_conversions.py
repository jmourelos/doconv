import doconv
from doconv.doconv import PluginManager
from doconv import log
from networkx import nx
import logging

log.level = logging.DEBUG

# Actually, this is not a test. It is just a convenient way to generate a graph with
# the conversions provided by doconv.
def test_generate_conversions():
    logger = log.setup_custom_logger('root')
    doconv.__dict__['logger'] = logger

    plugin_manager = PluginManager()
    nx.nx_pydot.write_dot(plugin_manager.graph, 'conversions.dot')
    
    # Generate a dot file instead of svg to minimize the growth of the git
    # repository. Let this code for future reference.
    #from pygraphviz import AGraph
    #A = nx.to_agraph(G)
    # A.layout()
    #A.draw('conversions.svg', prog="circo")

def main():
    test_generate_conversions()

if __name__ == "__main__":
    main()
