import networkx as nx
import matplotlib.pyplot as plt


def plot_dfa(Q, Sigma, delta, q0, F):
    G = nx.DiGraph()

    for state in Q:
        G.add_node(state, shape='doublecircle' if state in F else 'circle')

    trans = {}
    for state, transitions in delta.items():
        for symbol, next_states in transitions.items():
            for next_state in next_states:
                trans.setdefault(state, {}).setdefault(next_state, []).append(symbol)

    for state, next_state in trans.items():
        for next_state, symbols in next_state.items():
            G.add_edge(state, next_state, label=','.join(symbols))
    pos = nx.spring_layout(G)

    # Draw nodes
    node_border_widths = [3 if state in F else 1 for state in G.nodes()]
    node_labels = {state: state for state in G.nodes()}
    nx.draw_networkx_nodes(G, pos, node_color='white', edgecolors='black', linewidths=node_border_widths, node_size=1000, alpha=0.75)
    nx.draw_networkx_labels(G, pos, labels=node_labels, verticalalignment='top')

    # Draw edges
    edge_labels = {(n1, n2): d['label'] for n1, n2, d in G.edges(data=True)}
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.5, font_size=8, font_color='red')

    plt.title('DFA')
    plt.axis('off')
    plt.show()


# Example usage
Q = ['q0', 'q1', 'q2']
Sigma = ['a', 'b']
delta = {
    'q0': {'a': ['q0', 'q1'], 'b': ['q0']},
    'q1': {'a': ['q0'], 'b': ['q2']},
    'q2': {'b': ['q2']}
}
q0 = 'q0'
F = ['q2']

plot_dfa(Q, Sigma, delta, q0, F)
