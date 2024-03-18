import re

TOKENS = {
    'IDENTIFIER': r'[a-zA-Z][a-zA-Z0-9_]*',
    'INTEGER': r'\d+',
    'FLOAT': r'\d+\.\d+',
    'DOT': r'\.',
    'COMMA': r',',
    'STRING': r'\'[a-zA-Z\s][a-zA-Z\s]+\'',
    'CHAR': r'\'[a-zA-Z]\'',
    'INCREMENT': r'\+=',
    'PLUS': r'\+',
    'MINUS': r'-',
    'MULTIPLY': r'\*',
    'DIVIDE': r'/',
    'LPAREN': r'\(',
    'RPAREN': r'\)',
    'EQUAL': r'==',
    'LESS_EQUAL': r'<=',
    'GREATER_EQUAL': r'>=',
    'LESS': r'<',
    'GREATER': r'>',
    'ASSIGN': r'=',
    'COLON': r':',
    'SPACE': r'\s+',
    'NEWLINE': r'\n'
}

KEY_WORDS = ['if', 'else', 'while', 'for', 'return', 'break', 'continue']


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {self.value})"

    def __repr__(self):
        return self.__str__()


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception("Invalid character")

    def get_next_token(self):
        while self.pos < len(self.text):
            for token_type, pattern in TOKENS.items():
                regex = re.compile(pattern)
                match = regex.match(self.text, self.pos)
                if match:
                    value = match.group(0)
                    self.pos = match.end()
                    if token_type == 'SPACE' or token_type == 'NEWLINE':
                        break  # Skip spaces
                    elif value in KEY_WORDS:
                        return Token(value.upper(), value)
                    else:
                        return Token(token_type, value)
            else:
                self.error()

        return Token('EOF', None)

class Parser:
    def __init__(self, text):
        self.text = text
        self.tokens = []
        pass

    def parse(self):
        lexer = Lexer(self.text)
        while True:
            token = lexer.get_next_token()
            if token.type == 'EOF':
                break
            self.tokens.append(token)

    def print_tokens(self):
        for token in self.tokens:
            print(token)



if __name__ == '__main__':
    while True:
        text = input("input> ")
        if text == "q":
            break
        parser = Parser(text)
        parser.parse()
        parser.print_tokens()
        print("\n")


