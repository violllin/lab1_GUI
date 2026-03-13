class Token:
    def __init__(self, code, type_name, lexeme, line, start, end, is_error=False):
        self.code = code
        self.type_name = type_name
        self.lexeme = lexeme
        self.line = line
        self.start = start
        self.end = end
        self.is_error = is_error


class Scanner:
    def __init__(self):
        self.keywords = {
            "Int": (1, "ключевое слово"),
            "String": (2, "ключевое слово"),
            "return": (3, "ключевое слово"),
            "let": (4, "ключевое слово"),
            "in": (5, "ключевое слово"),
            "Bool": (7, "ключевое слово"),
            "Float": (8, "ключевое слово")
        }

        self.single_chars = {
            ':': (11, "разделитель"),
            '+': (12, "оператор"),
            '*': (13, "оператор"),
            '=': (15, "оператор"),
            '(': (16, "разделитель"),
            ')': (17, "разделитель"),
            ',': (18, "разделитель"),
            '{': (19, "разделитель"),
            '}': (20, "разделитель"),
            ';': (21, "разделитель"),
            '%': (23, "оператор"),
            '/': (24, "оператор")
        }

    def analyze(self, text):
        tokens = []
        i = 0
        line = 1
        col = 1

        while i < len(text):
            char = text[i]

            if char in '\t\n\r':
                if char == '\n':
                    line += 1
                    col = 1
                else:
                    col += 1
                i += 1
                continue

            start_col = col

            if char == ' ':
                tokens.append(Token(14, "разделитель", "space", line, start_col, col))
                i += 1
                col += 1
                continue

            if char.isalpha():
                lexeme = char
                i += 1
                col += 1
                while i < len(text) and text[i].isalpha():
                    lexeme += text[i]
                    i += 1
                    col += 1

                if lexeme in self.keywords:
                    code, type_name = self.keywords[lexeme]
                    tokens.append(Token(code, type_name, lexeme, line, start_col, col - 1))
                else:
                    tokens.append(Token(6, "идентификатор", lexeme, line, start_col, col - 1))
                continue

            if char.isdigit():
                lexeme = char
                i += 1
                col += 1
                while i < len(text) and text[i].isdigit():
                    lexeme += text[i]
                    i += 1
                    col += 1
                tokens.append(Token(22, "константа", lexeme, line, start_col, col - 1))
                continue

            if char == '-':
                if i + 1 < len(text) and text[i + 1] == '>':
                    tokens.append(Token(10, "оператор", "->", line, start_col, col + 1))
                    i += 2
                    col += 2
                else:
                    tokens.append(Token(9, "оператор", "-", line, start_col, col))
                    i += 1
                    col += 1
                continue

            if char in self.single_chars:
                code, type_name = self.single_chars[char]
                tokens.append(Token(code, type_name, char, line, start_col, col))
                i += 1
                col += 1
                continue

            tokens.append(Token("ERROR", "недопустимый символ", char, line, start_col, col, is_error=True))
            i += 1
            col += 1

        return tokens