# Determinism in Finite Automata. Conversion from NDFA 2 DFA. Chomsky Hierarchy.

### Course: Formal Languages & Finite Automata

### Author: Pascal Adrian

----

## Objectives:
1. Understand what an automaton is and what it can be used for.

2. Continuing the work in the same repository and the same project, the following need to be added:
    a. Provide a function in your grammar type/class that could classify the grammar based on Chomsky hierarchy.

    b. For this you can use the variant from the previous lab.

3. According to your variant number (by universal convention it is register ID), get the finite automaton definition and do the following tasks:

    a. Implement conversion of a finite automaton to a regular grammar.

    b. Determine whether your FA is deterministic or non-deterministic.

    c. Implement some functionality that would convert an NDFA to a DFA.
    
    d. Represent the finite automaton graphically (Optional, and can be considered as a __*bonus point*__):
      
    - You can use external libraries, tools or APIs to generate the figures/diagrams.
        
    - Your program needs to gather and send the data about the automaton and the lib/tool/API return the visual representation.

## Implementation description:

1. First, I modified a bit the `Grammar` class, to accept the grammar information at the creation time.

2. Then in a separated file, I crated a second class named `ExtendedGrammar` that inherits from `Grammar` and adds the 
functionality to classify the grammar based on Chomsky hierarchy. To check the grammar type, I created 5 additional
methods:
    - `check_type_3`
    - `check_type_2`
    - `check_type_1`
    - `check_grammar_validity`
    - `check_Chomsky_type`

3. The `check_type_3` method checks if the grammar is of type 3 (regular) and what type of it is left or right. 
It does this by first checking if each production has the form `A -> aB` or `A -> a` or `A -> Ba` and flags the grammar
as left or right regular. If both or none of the flags are set, the grammar is not regular. And if one of the flags is
set, the grammar is marked as `Type 3` and the corresponding subtype `(Left)` or `(Right)`.

```
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
                    if production[0] not in self.VT and production[0] != '':
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
```

4. The `check_type_2` method checks if the grammar is of type 2 (context-free). It does this by checking if the left side
of the production rule is a single non-terminal symbol.

```
 def check_type_2(self, explicit=False):
        for state, productions in self.P.items():
            if state not in self.VN:
                if explicit:
                    print(f"All the states must be non-terminal symbols, thus the grammar is not of type 2")
                return False
        if explicit:
            print("Grammar is of type 2")
        return self.types[3]
```

5. The `check_type_1` method checks if the grammar is of type 1 (context-sensitive). It does this by checking if it is 
a monotonous grammar. A grammar is monotonous if the length of the left side of the production rule is less or equal to
the length of the right side of the production rule. Also, it checks if all the states contain at least one non-terminal
symbol. This method was inspired by the definition of a context-sensitive grammar from the book "Intelligence Science" by
Zhongzhi Shi, 2021.

```
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
```
