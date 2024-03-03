from Lab_1.Lab_1 import Grammar


class ExtendedGrammar(Grammar):
    def __init__(self, VN, VT, P):
        super().__init__(VN, VT, P)
        self.types = ['Invalid', 'Type 0', 'Type 1', 'Type 2', 'Type 3 (Left)', 'Type 3 (Right)']
        self.type = self.check_Chomsky_type()

    def check_grammar_validity(self, explicit=False):
        def check_symbols(string):
            for symbol in string:
                if symbol not in self.VN and symbol not in self.VT and symbol != '':
                    return False
            return True

        for state, productions in self.P.items():
            if not check_symbols(state):
                if explicit:
                    print(f"Invalid symbol in state {state}")
                return False
            for production in productions:
                if not check_symbols(production):
                    if explicit:
                        print(f"Invalid symbol in production {production}")
                    return False

        if not self.VN or not self.VT or not self.P:
            if explicit:
                print("VN and VT and P can not be empty")
            return False

        return True

    def check_type_3(self, explicit=False):
        left = False
        right = False

        for state, productions in self.P.items():
            if state not in self.VN:
                if explicit:
                    print(f"Grammar is not of type 3 because of state {state}")
                return False
            for production in productions:
                if len(production) > 2:
                    if explicit:
                        print(f"Grammar is not of type 3 because of production {production}")
                    return False

                if len(production) == 2:
                    if production[0] in self.VN and production[1] in self.VT:
                        left = True

                    elif production[0] in self.VT and production[1] in self.VN:
                        right = True

                    else:
                        if explicit:
                            print(f"Grammar is not of type 3 because of production {production}")
                        return False

                if len(production) < 2:
                    if production[0] not in self.VT:
                        if explicit:
                            print(f"Grammar is not of type 3 because of production {production}")
                        return False

        if left and right:
            if explicit:
                print("Grammar is not of type 3 because it has both left and right productions")
            return False

        if not left and not right:
            if explicit:
                print("Grammar is not of type 3")
            return False

        if left and not right:
            if explicit:
                print("Grammar is of type 3 (Left)")
            return self.types[4]

        if right and not left:
            if explicit:
                print("Grammar is of type 3 (Right)")
            return self.types[5]

    def check_type_2(self, explicit=False):
        for state, productions in self.P.items():
            if state not in self.VN:
                if explicit:
                    print(f"All the states must be non-terminal symbols, thus the grammar is not of type 2")
                return False
        if explicit:
            print("Grammar is of type 2")
        return self.types[3]

    def check_type_1(self, explicit=False):
        def check_for_non_terminal(string):
            for symbol in string:
                if symbol in self.VN:
                    return True
            return False

        for state, productions in self.P.items():
            if not check_for_non_terminal(state):
                if explicit:
                    print(f"All the states must contain at least one non-terminal symbol"
                          f", thus the grammar is not of type 1")
                return False
            for production in productions:
                if len(state) > len(production):
                    if explicit:
                        print(f"The grammar is not monotonous, thus it can not be of type 1")
                    return False
        if explicit:
            print("Grammar is of type 1")
        return self.types[2]

    def check_Chomsky_type(self):
        if self.check_grammar_validity():
            if self.check_type_3() == self.types[5]:
                return self.types[5]
            if self.check_type_3() == self.types[4]:
                return self.types[4]
            if self.check_type_2():
                return self.types[3]
            if self.check_type_1():
                return self.types[2]
            return self.types[1]
        return self.types[0]

    def __str__(self):
        return f"VN: {self.VN}\nVT: {self.VT}\nP: {self.P}\nType: {self.type}\n"



def main():
    VN = {'S', 'B', 'C'}
    VT = {'a', 'b', 'c'}
    P = {
        'S': ['aB'],
        'B': ['aC', 'bB'],
        'C': ['bB', 'c', 'aS']
    }
    grammar = ExtendedGrammar(VN, VT, P)
    print(grammar)

    VN = {'S', 'B', 'C'}
    VT = {'a', 'b', 'c'}
    P = {
        'S': ['Ba'],
        'B': ['Ca', 'Bb'],
        'C': ['Bb', 'c', 'Sa']
    }
    grammar = ExtendedGrammar(VN, VT, P)
    print(grammar)

    VN = {'S', 'B', 'C'}
    VT = {'a', 'b', 'c'}
    P = {
        'S': ['aB'],
        'B': ['aC', 'Bb'],
        'C': ['Bb', 'c', 'Sa']
    }
    grammar = ExtendedGrammar(VN, VT, P)
    print(grammar)

    VN = {'S', 'A', 'B'}
    VT = {'a', 'b', 'c'}
    P = {
        'S': ['aSAB', 'aAB'],
        'BA': ['AB'],
        'aA': ['ab'],
        'bA': ['bb'],
        'bB': ['bc'],
        'cB': ['cc'],
    }
    grammar = ExtendedGrammar(VN, VT, P)
    print(grammar)

    VN = {'S', 'A', 'B'}
    VT = {'a', 'b', 'c'}
    P = {
        'S': ['aSAB', 'aAB'],
        'BA': ['AB'],
        'aA': ['ab'],
        'bA': ['bb'],
        'bB': ['bc'],
        'CB': ['cc'],
    }
    grammar = ExtendedGrammar(VN, VT, P)
    print(grammar)

    VN = {'S', 'A', 'B'}
    VT = {'a', 'b', 'c'}
    P = {}
    grammar = ExtendedGrammar(VN, VT, P)
    print(grammar)


if __name__ == "__main__":
    main()
