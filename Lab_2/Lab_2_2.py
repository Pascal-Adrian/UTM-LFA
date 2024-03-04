from Lab_2.Lab_2_1 import ExtendedGrammar
import networkx as nx
import matplotlib.pyplot as plt
import graphviz


class FiniteAutomaton:
    def __init__(self, Q, Sigma, delta, q0, F):
        self.Q = Q
        self.Sigma = Sigma
        self.delta = delta
        self.q0 = q0
        self.F = F
        self.type = self.check_DFA_or_NFA()
        self.grammar = self.convert_to_grammar()
        self.plot_count = 0

    def convert_to_grammar(self):
        alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                    'Q', 'R', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        VN = []
        VN.append('S')
        for i in range(1, len(self.Q)):
            VN.append(alphabet[i])
        Q_to_VN = dict(zip(self.Q, VN))
        VT = self.Sigma
        P = {}
        for state, transitions in self.delta.items():
            for symbol, next_state in transitions.items():
                for next in next_state:
                    if Q_to_VN[state] not in P:
                        P[Q_to_VN[state]] = []
                    P[Q_to_VN[state]].append(f"{symbol}{Q_to_VN[next]}")
                    if state in self.F and next in self.F:
                        P[Q_to_VN[state]].append(symbol)
        return ExtendedGrammar(VN, VT, P)

    def check_DFA_or_NFA(self):
        for state, transitions in self.delta.items():
            for symbol, next_state in transitions.items():
                if len(next_state) > 1:
                    return "NFA"
                if symbol == '':
                    return "NFA"
        return "DFA"

    def NFA_to_DFA(self):
        def epsilon_closure(states):
            epsilon_closure_states = set(states)
            stack = list(states)

            while stack:
                state = stack.pop()
                if state in self.delta and '' in self.delta[state]:
                    for s in self.delta[state]['']:
                        if s not in epsilon_closure_states:
                            epsilon_closure_states.add(s)
                            stack.append(s)

            return frozenset(epsilon_closure_states)

        def move(states, symbol):
            new_states = set()
            for state in states:
                if state in self.delta and symbol in self.delta[state]:
                    new_states.update(self.delta[state][symbol])
            return frozenset(new_states)

        dfa_states = set()
        dfa_transitions = {}
        dfa_final_states = set()

        queue = [epsilon_closure({self.q0})]
        dfa_states.add(queue[0])

        while queue:
            current_states = queue.pop(0)

            for symbol in self.Sigma:
                new_states = epsilon_closure(move(current_states, symbol))

                if new_states not in dfa_states:
                    queue.append(new_states)
                    dfa_states.add(new_states)

                dfa_transitions.setdefault(current_states, {})[symbol] = new_states

        for state in dfa_states:
            if state.intersection(self.F):
                dfa_final_states.add(state)

        dfa_states = {frozenset(state) for state in dfa_states}

        self.Q = dfa_states
        self.delta = dfa_transitions
        self.q0 = epsilon_closure({self.q0})
        self.F = dfa_final_states
        self.type = "DFA"

    def plot_nfa(self):
        G = nx.DiGraph()

        for state in self.Q:
            G.add_node(state, shape='doublecircle' if state in self.F else 'circle')

        trans = {}
        for state, transitions in self.delta.items():
            for symbol, next_states in transitions.items():
                for next_state in next_states:
                    trans.setdefault(state, {}).setdefault(next_state, []).append(symbol)

        for state, next_state in trans.items():
            for next_state, symbols in next_state.items():
                G.add_edge(state, next_state, label=','.join(symbols))
        pos = nx.spring_layout(G)

        # Draw nodes
        node_border_widths = [3 if state in self.F else 1 for state in G.nodes()]
        node_labels = {state: state for state in G.nodes()}
        nx.draw_networkx_nodes(G, pos, node_color='white', edgecolors='black', linewidths=node_border_widths, node_size=1000, alpha=0.75)
        nx.draw_networkx_labels(G, pos, labels=node_labels, verticalalignment='top')

        # Draw edges
        edge_labels = {(n1, n2): d['label'] for n1, n2, d in G.edges(data=True)}
        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.5, font_size=10)

        plt.title('NFA')
        plt.axis('off')
        plt.show()

    def plot_dfa(self):
        G = nx.DiGraph()

        # Add states
        for state in self.Q:
            G.add_node(state, shape='doublecircle' if state in self.F else 'circle')

        # Add transitions
        for state in self.Q:
            for symbol in self.Sigma:
                if self.delta[state].get(symbol):
                    next_state = self.delta[state][symbol]
                    G.add_edge(state, next_state, label=symbol)
        print(G.edges(data=True))
        pos = nx.spring_layout(G)

        # Draw nodes
        node_border_widths = [3 if state in self.F else 1 for state in G.nodes()]
        node_labels = {state: ''.join(sorted(list(state))) for state in G.nodes()}
        nx.draw_networkx_nodes(G, pos, node_color='white', node_size=1000, alpha=0.75, edgecolors='black',
                               linewidths=node_border_widths)
        nx.draw_networkx_labels(G, pos, labels=node_labels, verticalalignment='top')

        # Draw edges
        edge_labels = {(n1, n2): d['label'] for n1, n2, d in G.edges(data=True)}
        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.7)

        plt.title('DFA')
        plt.axis('off')
        plt.show()

    def __str__(self):
        return f"Q: {self.Q}\nSigma: {self.Sigma}\ndelta: {self.delta}\nq0: {self.q0}\nF: {self.F}\nType: {self.type}\n"


def main():
    Q = ['q0', 'q1', 'q2']
    sigma = ['a', 'b']
    F = ['q2']
    delta = {
        'q0': {'a': ['q0', 'q1'], 'b': ['q0']},
        'q1': {'a': ['q0'], 'b': ['q2']},
        'q2': {'b': ['q2']}
    }
    q0 = 'q0'
    fa = FiniteAutomaton(Q, sigma, delta, q0, F)
    fa.plot_nfa()
    print(fa)
    print(fa.grammar)
    fa.NFA_to_DFA()
    fa.plot_dfa()
    print(fa)


if __name__ == "__main__":
    main()