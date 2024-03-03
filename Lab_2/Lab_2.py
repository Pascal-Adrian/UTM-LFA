def FiniteAutomaton(Q, Sigma, delta, q0, F):
    def __init__(self, Q, Sigma, delta, q0, F):
        self.Q = Q
        self.Sigma = Sigma
        self.delta = delta
        self.q0 = q0
        self.F = F



def main():
    Q = ['q0', 'q1', 'q2']
    sigma = ['a', 'b']
    F = ['q2']
    delta = {
        'q0': {'a': ['q0', 'q1'], 'b': ['q0']},
        'q1': {'a': ['q0'], 'b': ['q2']},
        'q2': {'b': ['q2']}
    }

if __name__ == "__main__":
    main()