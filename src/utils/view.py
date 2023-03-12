# utils/view.py

import networkx as nx
import matplotlib.pyplot as plt
from prettytable import PrettyTable

class Colors:
    """
    shortcuts for printed color in the console.
    """

    def __init__(self):
        pass

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def visualize_tree(node, graph):
    """
    it visualizes a Merkle Tree using graphviz libraries
    :param node:
    :param graph:
    :return:
    """
    if 'data' in node:
        graph.node(node['hash'], label=node['data'])
    else:
        graph.node(node['hash'], label=node['hash'][:8])
        visualize_tree(node['left'], graph)
        graph.edge(node['hash'], node['left']['hash'])
        if 'right' in node:
            visualize_tree(node['right'], graph)
            graph.edge(node['hash'], node['right']['hash'])

def create_visualization_table(fields, row_list, title):
    """

    :param fields: list of fields of the table
    :param row_list: list of every row
    :param title : table title
    :return: PrettyTable object
    """
    table = PrettyTable()

    # Define the column fields
    table.field_names = fields

    # Add rows
    for r in row_list:
        table.add_row(r)

    # add title
    table.title = title
    return table


def visualize_blockchain(blocks, path="../vis/blockchain/blockchain.pdf"):
    """

    :param blocks:
    :param path:
    :return:
    """
    g = nx.DiGraph()
    # add nodes
    for b in blocks[-10:]:
        node_color = 'blue' if b.main_chain else 'orange'  # set node color based on parameter
        g.add_node(str(b.hash[:8]) + str(b.confirmed), transactions=b.transactions, nonce=b.nonce, time=b.time, creation_time=b.creation_time, color=node_color)

    # add edges
    for b in blocks:
        if b.prev is not None:
            g.add_edge(str(b.hash[:8]) + str(b.confirmed), str(b.prev[:8]) + str(b.confirmed))

    # draw graph
    pos = nx.spring_layout(g)
    nx.draw(g, pos, node_color='orange', with_labels=True)
    plt.savefig(path)