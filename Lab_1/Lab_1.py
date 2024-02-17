import random

class Grammar:
    def __init__(self):
        self.VN = {'S', 'B', 'C'}
        self.VT = {'a', 'b', 'c'}
        self.P = {
            'S': ['aB'],
            'B': ['aC', 'bB'],
            'C': ['bB', 'c', 'aS']
        }

    def generate_string(self):
        string = ''
        current_symbol = 'S'
        while current_symbol in self.VN:
            production = random.choice(self.P[current_symbol])
            for symbol in production:
                if symbol in self.VT:
                    string += symbol
                    current_symbol = ''
                else:
                    current_symbol = symbol
                    break
        return string

    def to_finite_automaton(self):
        Q = self.VN
        Sigma = self.VT
        delta = {}
        for state, productions in self.P.items():
            for production in productions:
                if len(production) == 1:
                    if production.islower():
                        delta.setdefault(state, {}).setdefault(production, [production])
                else:
                    delta.setdefault(state, {}).setdefault(production[0], []).append(production[1:])
        q0 = 'S'
        F = [t for production in self.P for t in self.P[production] if len(t) == 1 and t.islower()]
        return FiniteAutomaton(Q, Sigma, delta, q0, F)


class FiniteAutomaton:
    def __init__(self, Q, Sigma, delta, q0, F):
        self.Q = Q
        self.Sigma = Sigma
        self.delta = delta
        self.q0 = q0
        self.F = F

    def string_belongs_to_language(self, input_string, explicit=False):
        current_state = self.q0
        for symbol in input_string:
            if symbol not in self.Sigma:
                if explicit:
                    print("Invalid symbol in input string")
                return False
            if symbol in self.delta.get(current_state, {}):
                current_state = self.delta[current_state][symbol][0]
            else:
                if explicit:
                    print("Invalid transition")
                return False
        return current_state in self.F

    def __str__(self):
        return f"Q: {self.Q}\nSigma: {self.Sigma}\ndelta: {self.delta}\nq0: {self.q0}\nF: {self.F}"

grammar = Grammar()
automaton = grammar.to_finite_automaton()
print(automaton)

for _ in range(10):
    generated_string = grammar.generate_string()
    print("\n=======================================")
    print("Generated string:", generated_string)
    print("String belongs to language:", automaton.string_belongs_to_language(generated_string))

for _ in range(3):
    generated_string = grammar.generate_string()
    random_index = random.randint(0, len(generated_string))
    generated_string = generated_string[:random_index] + 'd' + generated_string[random_index:]
    print("\n=======================================")
    print("Generated string:", generated_string)
    print("String belongs to language:", automaton.string_belongs_to_language(generated_string, True))

for _ in range(10):
    random_string = ''.join(random.choices(list(grammar.VT), k=10))
    print("\n=======================================")
    print("Generated string:", random_string)
    print("String belongs to language:", automaton.string_belongs_to_language(random_string, True))

for _ in range(3):
    generated_string = grammar.generate_string()
    print("\n=======================================")
    print("Generated string:", generated_string)
    random_index = random.randint(0, len(generated_string))
    print("Removing symbol at index", random_index)
    generated_string = generated_string[:random_index] + generated_string[random_index + 1:]
    print("Modified string:", generated_string)
    print("String belongs to language:", automaton.string_belongs_to_language(generated_string, True))



