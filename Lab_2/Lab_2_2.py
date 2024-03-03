from Lab_2.Lab_2_1 import ExtendedGrammar
import networkx as nx
import matplotlib.pyplot as plt


class FiniteAutomaton:
    def __init__(self, Q, Sigma, delta, q0, F):
        self.Q = Q
        self.Sigma = Sigma
        self.delta = delta
        self.q0 = q0
        self.F = F
        self.type = self.check_DFA_or_NFA()
        self.grammar = self.convert_to_grammar()

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

    def convert_to_dfa(self):
        def epsilon_closure(states, delta):
            e_closure = set(states)
            stack = list(states)
            while stack:
                state = stack.pop()
                transitions = delta.get(state, {}).get('', [])
                for transition in transitions:
                    if transition not in e_closure:
                        e_closure.add(transition)
                        stack.append(transition)
            return frozenset(e_closure)

        def move(states, symbol, delta):
            moves = set()
            for state in states:
                transitions = delta.get(state, {}).get(symbol, [])
                moves.update(transitions)
            return frozenset(moves)

        dfa_states = set()
        dfa_delta = {}
        dfa_start_state = epsilon_closure({self.q0}, self.delta)
        dfa_states.add(dfa_start_state)
        stack = [dfa_start_state]

        while stack:
            current_states = stack.pop()
            for symbol in self.Sigma:
                next_states = epsilon_closure(move(current_states, symbol, self.delta), self.delta)
                if next_states:
                    dfa_delta[current_states, symbol] = next_states
                    if next_states not in dfa_states:
                        dfa_states.add(next_states)
                        stack.append(next_states)

        self.Q = dfa_states
        self.delta = dfa_delta
        self.type = "DFA"

    def plot_automaton(self):
        G = nx.DiGraph()

        # Add nodes and edges
        for (current_states, symbol), next_states in self.delta.items():
            for next_state in next_states:
                G.add_edge(current_states, next_state, label=symbol)

        # Plot the graph as a tree
        plt.figure(figsize=(8, 6))
        pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
        nx.draw(G, pos, with_labels=True, arrows=True)
        edge_labels = {(current_states, next_state): symbol for (current_states, symbol), next_state in
                       self.delta.items()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
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
    fa.plot_automaton()
    print(fa)
    print(fa.grammar)
    fa.convert_to_dfa()
    # fa.plot_automaton()
    print(fa)


if __name__ == "__main__":
    main()