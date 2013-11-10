import doconv
from doconv import log
from networkx import nx


# Actually, this is not a test. It is just a fast way to generate a graph with
# the conversions provided by doconv.
def test_generate_conversions():
    logger = log.setup_custom_logger('root')
    doconv.__dict__['logger'] = logger

    G = doconv.create_graph()
    nx.write_dot(G, 'conversions.dot')

    # Generate a dot file instead of svg to minimize the growth of the git
    # repository. Let this code for future reference.
    #from pygraphviz import AGraph
    #A = nx.to_agraph(G)
    # A.layout()
    #A.draw('conversions.svg', prog="circo")
