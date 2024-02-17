# Regular Grammars & Finite Automata

### Course: Formal Languages & Finite Automata

### Author: Pascal Adrian

----

## Objectives:
1. Discover what a language is and what it needs to have in order to be considered a formal one;

2. Provide the initial setup for the evolving project that you will work on during this semester. You can deal with each laboratory work as a separate task or project to demonstrate your understanding of the given themes, but you also can deal with labs as stages of making your own big solution, your own project. Do the following:

    a. Create GitHub repository to deal with storing and updating your project;

    b. Choose a programming language. Pick one that will be easiest for dealing with your tasks, you need to learn how to solve the problem itself, not everything around the problem (like setting up the project, launching it correctly and etc.);

    c. Store reports separately in a way to make verification of your work simpler (duh)

3. According to your variant number, get the grammar definition and do the following:

    a. Implement a type/class for your grammar;

    b. Add one function that would generate 5 valid strings from the language expressed by your given grammar;

    c. Implement some functionality that would convert and object of type Grammar to one of type Finite Automaton;

    d. For the Finite Automaton, please add a method that checks if an input string can be obtained via the state transition from it;

----

## Implementation description:

1. As sugested in the task I created a object to contain the methods and attributes of the grammar. The object is called `Grammar` and it contains the following attributes:
    - `VN` - a set of non-terminal symbols;
    - `VT` - a set of terminal symbols;
    - `P` - a dictionary containing the production rules of the grammar;

```
class Grammar:
    def __init__(self):
        self.VN = {'S', 'B', 'C'}
        self.VT = {'a', 'b', 'c'}
        self.P = {
            'S': ['aB'],
            'B': ['aC', 'bB'],
            'C': ['bB', 'c', 'aS']
        }
```

2. The `generate_string` method is used to generate valid strings from the language expressed by the given grammar. The function works by starting from the start symbol and then randomly choosing a production rule from the ones allowed by the grammar for this symbol and adding the symbols to the string. If the symbol is a terminal symbol the function stops, otherwise it continues with the next symbol in the production rule.

```
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
```

3. The `convert_to_finite_automaton` method is used to convert the grammar to a finite automaton. The method creates a finite automaton and initiates a FiniteAutomaton object with the following attributes:
    - `Q` - a set of states;
    - `Sigma` - a set of input symbols;
    - `delta` - a dictionary containing the state transitions;
    - `q0` - the initial state;
    - `F` - a set of final states;

    The method works by iterating through the production rules and adding the state transitions to the delta dictionary. The initial state is set to 'S' and the final states are set to the terminal symbols.

```
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
```

4. The `string_belongs_to_language` method is used to check if an input string can be obtained via the state transition from the finite automaton. The method works by iterating through the input string and checking if character and the state transition is valid. If the state transition is not valid the method returns False, otherwise it returns True. Also, if the explicit parameter is set to True the method will print the reason why the string is not valid.

```
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
```

----

## Results:

### The obtained finite automaton:

```
Q: {'S', 'B', 'C'}
Sigma: {'c', 'a', 'b'}
delta: {'S': {'a': ['B']}, 'B': {'a': ['C'], 'b': ['B']}, 'C': {'b': ['B'], 'c': ['c'], 'a': ['S']}}
q0: S
F: ['c']
```

### In order to test the implementation I created a couple loops that generate strings and check if they belong to the language:

1. First with valid strings, generated by the grammar and as expected all the strings belong to the language.

```
=======================================
Generated string: ababbabbabbabbbac
String belongs to language: True

=======================================
Generated string: aabbac
String belongs to language: True

=======================================
Generated string: abbaaababac
String belongs to language: True

=======================================
Generated string: aac
String belongs to language: True

=======================================
Generated string: aaaaabac
String belongs to language: True

=======================================
Generated string: abaaabac
String belongs to language: True

=======================================
Generated string: aac
String belongs to language: True

=======================================
Generated string: aabbbbac
String belongs to language: True

=======================================
Generated string: abac
String belongs to language: True

=======================================
Generated string: abbac
String belongs to language: True
```

2. Then with invalid strings, generated randomly and as expected all the strings did not belong to the language.

```
=======================================
Generated string: bacacacbac
Invalid transition
String belongs to language: False

=======================================
Generated string: abbccabbcc
Invalid transition
String belongs to language: False

=======================================
Generated string: bbcbabcaba
Invalid transition
String belongs to language: False

=======================================
Generated string: abccbaccaa
Invalid transition
String belongs to language: False

=======================================
Generated string: baacbababa
Invalid transition
String belongs to language: False

=======================================
Generated string: acccbacabc
Invalid transition
String belongs to language: False

=======================================
Generated string: accbbcacca
Invalid transition
String belongs to language: False

=======================================
Generated string: abbbbabbab
String belongs to language: False

=======================================
Generated string: baabacabca
Invalid transition
String belongs to language: False

=======================================
Generated string: abaacbbbac
Invalid transition
String belongs to language: False
```

3. Then with invalid strings, generated by the grammar and then modified by adding an invalid character and as expected all the strings did not belong to the language.
```
=======================================
Generated string: adbac
Invalid symbol in input string
String belongs to language: False

=======================================
Generated string: dababac
Invalid symbol in input string
String belongs to language: False

=======================================
Generated string: aabbbbbbbbabdbac
Invalid symbol in input string
String belongs to language: False
```

4. And finally with invalid strings, generated by the grammar and then modified by removing a character and as expected there were some strings that did belong to the language and some that did not. This is because the grammar has some repetitive production rules and removing a character can result in a valid string.
```
=======================================
Generated string: ababbbaaaabaaababac
Removing symbol at index 10
Modified string: ababbbaaaaaaababac
String belongs to language: True

=======================================
Generated string: abbac
Removing symbol at index 0
Modified string: bbac
Invalid transition
String belongs to language: False

=======================================
Generated string: aac
Removing symbol at index 0
Modified string: ac
Invalid transition
String belongs to language: False
```

----

## Conclusion:

Throughout this exploration of regular grammars and finite automata, I've delved into the core concepts of formal languages and computational models. By implementing a grammar object and transforming it into a finite automaton, I've gained a deeper understanding of language generation and recognition processes. Through rigorous testing, I've verified the robustness of the implemented solutions, ensuring they accurately reflect the underlying grammar's rules. This journey has not only equipped me with practical programming skills but also cultivated a sharper analytical mindset essential for tackling complex computational problems. As I conclude this phase, I anticipate further growth and application of these foundational concepts in my journey through formal language theory.