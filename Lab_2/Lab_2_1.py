from Lab_1.Lab_1 import Grammar

class ExtendedGrammar(Grammar):
    def __init__(self, VN, VT, P):
        super().__init__(VN, VT, P)
        self.types = ['Type 0', 'Type 1', 'Type 2', 'Type 3']

    def check_type_0(self):
        for state, productions in self.P.items():
            print(state, productions)
            for production in productions:
                print(production)
                if state in production:
                    print(state, production)
                    return False
            print('====================================')
        return True







def main():
    VN = {'S', 'B', 'C'}
    VT = {'a', 'b', 'c'}
    P = {
        'S': ['aB'],
        'B': ['aC', 'bB'],
        'C': ['bB', 'c', 'aS']
    }
    grammar = Grammar(VN, VT, P)

