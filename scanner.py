class Token:
    def __init__(self, code, type_name, value, line, start, end):
        self.code = code
        self.type_name = type_name
        self.value = value
        self.line = line
        self.start = start
        self.end = end

class LexicalError:
    def __init__(self, message, line, column, lexeme):
        self.message = message
        self.line = line
        self.column = column
        self.lexeme = lexeme

class Scanner:
    def __init__(self):
        self.codes = {
            'id': 1,
            'num': 2,
            '+': 3,
            '-': 4,
            '*': 5,
            '/': 6,
            '%': 7,
            '(': 8,
            ')': 9,
            'space': 10,
            'EOF': 11,
            'ERROR': 999
        }

    def analyze(self, text):
        tokens = []
        errors = []
        line = 1
        col = 1
        i = 0
        n = len(text)

        while i < n:
            char = text[i]

            if char.isalpha() or char == '_':
                start_col = col
                start_i = i
                while i < n and (text[i].isalnum() or text[i] == '_'):
                    i += 1
                    col += 1
                value = text[start_i:i]
                tokens.append(Token(self.codes['id'], 'Identifier', value, line, start_col, col - 1))
                continue

            if char.isdigit():
                start_col = col
                start_i = i
                while i < n and text[i].isdigit():
                    i += 1
                    col += 1
                value = text[start_i:i]
                tokens.append(Token(self.codes['num'], 'Number', value, line, start_col, col - 1))
                continue

            if char == '+':
                tokens.append(Token(self.codes['+'], 'Operator', '+', line, col, col))
                i += 1; col += 1; continue
            if char == '-':
                tokens.append(Token(self.codes['-'], 'Operator', '-', line, col, col))
                i += 1; col += 1; continue
            if char == '*':
                tokens.append(Token(self.codes['*'], 'Operator', '*', line, col, col))
                i += 1; col += 1; continue
            if char == '/':
                tokens.append(Token(self.codes['/'], 'Operator', '/', line, col, col))
                i += 1; col += 1; continue
            if char == '%':
                tokens.append(Token(self.codes['%'], 'Operator', '%', line, col, col))
                i += 1; col += 1; continue
            if char == '(':
                tokens.append(Token(self.codes['('], 'Bracket', '(', line, col, col))
                i += 1; col += 1; continue
            if char == ')':
                tokens.append(Token(self.codes[')'], 'Bracket', ')', line, col, col))
                i += 1; col += 1; continue

            if char in ' \t\r':
                tokens.append(Token(self.codes['space'], 'Space', ' ', line, col, col))
                i += 1; col += 1; continue

            if char == '\n':
                tokens.append(Token(self.codes['space'], 'Space', '\\n', line, col, col))
                i += 1
                line += 1
                col = 1
                continue

            errors.append(LexicalError(f"Unknown character: {char}", line, col, char))
            tokens.append(Token(self.codes['ERROR'], 'Error', char, line, col, col))
            i += 1
            col += 1

        tokens.append(Token(self.codes['EOF'], 'EOF', 'EOF', line, col, col))
        return tokens, errors