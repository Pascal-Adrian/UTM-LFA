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

6. The `check_grammar_validity` method checks if the grammar is valid. It does this by checking if all production rules
contain valid terminal and non-terminal characters.

```
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
```

7. The `check_Chomsky_type` method checks the grammar type based on the previous methods. It does this by calling the
previous methods and checking the return value in a cascading way. If the grammar is not valid, it returns `Invalid`.
If the grammar is of type 3, it returns the subtype. If the grammar is of type 2, it returns `Type 2`. If the grammar is
of type 1, it returns `Type 1`. If none of the previous conditions are met, it returns `Type 0`.

```
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
```

8. Also, I overrided the `__str__` method to print the grammar type. And applied to the grammar from the previous 
laboratory work and a couple of other grammars. The results are shown below:

```
VN: {'S', 'B', 'C'}
VT: {'b', 'c', 'a'}
P: {'S': ['aB'], 'B': ['aC', 'bB'], 'C': ['bB', 'c', 'aS']}
Type: Type 3 (Right)

VN: {'S', 'B', 'C'}
VT: {'b', 'c', 'a'}
P: {'S': ['Ba'], 'B': ['Ca', 'Bb'], 'C': ['Bb', 'c', 'Sa']}
Type: Type 3 (Left)

VN: {'S', 'B', 'C'}
VT: {'b', 'c', 'a'}
P: {'S': ['aB'], 'B': ['aC', 'Bb'], 'C': ['Bb', 'c', 'Sa']}
Type: Type 2

VN: {'S', 'A', 'B'}
VT: {'b', 'c', 'a'}
P: {'S': ['aSAB', 'aAB'], 'BA': ['AB'], 'aA': ['ab'], 'bA': ['bb'], 'bB': ['bc'], 'cB': ['cc']}
Type: Type 1

VN: {'S', 'A', 'B'}
VT: {'b', 'c', 'a'}
P: {'S': ['aSAB', 'aAB'], 'BA': ['AB'], 'aA': ['ab'], 'bA': ['bb'], 'bB': ['bc'], 'CB': ['cc']}
Type: Invalid

VN: {'S', 'A', 'B'}
VT: {'b', 'c', 'a'}
P: {}
Type: Invalid
```

9. Then, I created a new class named `FiniteAutomaton` that accepts the automaton information at the creation time and 
created a method that converts the `FiniteAutomaton` to a regular grammar. The method does this by creating the grammar
rules `VN`, `VT`, and `P` based on the automaton transitions returning a `ExtendedGrammar` object initialized with the 
rules. For a easier understanding I changed the `qn` notation with upper case letters.

```
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
```

10. Then, I created a method that checks if the automaton is deterministic or non-deterministic. It does this by checking
if the automaton has more than one transition for the same state and symbol or has `Ɛ` transition.

```
    def check_DFA_or_NFA(self):
        for state, transitions in self.delta.items():
            for symbol, next_state in transitions.items():
                if len(next_state) > 1:
                    return "NFA"
                if symbol == '':
                    return "NFA"
        return "DFA"
```

11. Then, I created a method that converts the non-deterministic finite automaton to a deterministic finite automaton. 
To do this, I created 2 additional methods: `epsilon_closure` and `move`, are defined to compute the epsilon closure and 
move for a given set of states and input symbol. `epsilon_closure` calculates all states reachable from a given set of 
states through epsilon transitions. `move` calculates the set of states reachable from a given set of states using a 
specific input symbol. 
The algorithm starts with the epsilon closure of the initial state of the NFA and adds it to the DFA states set.
It iterates through each state in the DFA states set:
For each input symbol in the alphabet, it computes the epsilon closure of the states reachable from the current DFA 
state using that input symbol.
If the resulting set of states is not already in the DFA states set, it adds it and enqueues it for further 
exploration.
It records the transition from the current DFA state to the new set of states in the DFA transitions dictionary.
Finally, it identifies the final states of the DFA based on whether they contain any final states of the NFA.

```
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
```

12. Then, I created a method that represents the finite automaton graphically. I used the `graphviz` app and `pygraphviz`
with the `networkx` library to create the graph. The method creates a graph with the states and transitions of the finite
automaton. 
```
```

13. Finally, I tested the implementation with the automaton corresponding to my variant number and I printed the results
and graphed the automatas. The results are shown below:

```
Q: ['q0', 'q1', 'q2']
Sigma: ['a', 'b']
delta: {'q0': {'a': ['q0', 'q1'], 'b': ['q0']}, 'q1': {'a': ['q0'], 'b': ['q2']}, 'q2': {'b': ['q2']}}
q0: q0
F: ['q2']
Type: NFA

VN: ['S', 'B', 'C']
VT: ['a', 'b']
P: {'S': ['aS', 'aB', 'bS'], 'B': ['aS', 'bC'], 'C': ['bC', 'b']}
Type: Type 3 (Right)

Q: {frozenset({'q2', 'q0'}), frozenset({'q0'}), frozenset({'q1', 'q0'})}
Sigma: ['a', 'b']
delta: {frozenset({'q0'}): {'a': frozenset({'q1', 'q0'}), 'b': frozenset({'q0'})}, frozenset({'q1', 'q0'}): {'a': frozenset({'q1', 'q0'}), 'b': frozenset({'q2', 'q0'})}, frozenset({'q2', 'q0'}): {'a': frozenset({'q1', 'q0'}), 'b': frozenset({'q2', 'q0'})}}
q0: frozenset({'q0'})
F: {frozenset({'q2', 'q0'})}
Type: DFA
```

[![Alt Text](Lab_2/NFA_Graph.png)]
[![Alt Text](Lab_2/DFA_Graph.png)]

## Conclusion:
Through this lab, I delved into the complexities of formal languages and automata. By extending the grammar class,
I classified grammars based on Chomsky hierarchy, providing invaluable insights into their structures. Converting finite
automata from non-deterministic to deterministic showcased the practical implications of theoretical concepts. 
Implementing methods for grammar validation and type checking enriched my understanding of language classification. 
Graphical representation aided visualization, enhancing comprehension. This hands-on exploration deepened my grasp of 
finite automata determinism and grammar classification, bridging theory with application.