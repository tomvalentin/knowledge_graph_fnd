import matplotlib.pyplot as plt
import networkx as nx

def printGraph(triples):
    G = nx.DiGraph(directed=True)
    for triple in triples:
        G.add_node(triple[0])
        G.add_node(triple[1])
        G.add_node(triple[2])
        G.add_edge(triple[0], triple[1])
        G.add_edge(triple[1], triple[2])

    pos = nx.spring_layout(G)
    plt.figure()
    nx.draw_networkx(G, pos, edge_color='black', width=1, linewidths=1,
            node_size=4000, node_color='#008dbe', alpha=0.9, arrows=True,
            labels={node: node for node in G.nodes()})
    plt.axis('off')
    plt.show()

triples = []
triples.append(['Sweden', 'located in', 'Europe'])
triples.append(['Sweden', 'is a', 'Country'])
triples.append(['Stockholm', 'capital of', 'Sweden'])


printGraph(triples)
