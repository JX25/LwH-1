import matplotlib.pyplot as plt
import networkx as nx


def create_graph(actions):
        graph = nx.Graph()
        for action in actions:
            for pred in action.predecessors:
                graph.add_edge(pred, action.name, weight=[act.duration for act in actions if act.name == pred][0])

        for action in actions:
            graph.add_node(action.name, size=10)

        pos = nx.spring_layout(graph)
        # nodes
        nx.draw_networkx(graph, pos, node_size=200)

        # edges
        nx.draw_networkx_nodes(graph, pos, graph.edges, width=3)

        # labels

        nx.draw_labels(graph, pos, font_size=20, font_family='sans-serif')

        plt.axis('off')
        plt.show()
