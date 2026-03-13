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
            "Int": (1, "ключевое слово 'Int'"),
            "var": (2, "ключевое слово 'var'"),
            "return": (3, "ключевое слово 'return'"),
            "let": (4, "ключевое слово 'let'"),
            "in": (5, "ключевое слово 'in'")
        }

        self.single_chars = {
            ':': (9, "двоеточие"),
            '+': (10, "оператор '+'"),
            '*': (11, "оператор '*'"),
            '=': (13, "оператор присваивания '='"),
            '(': (14, "открывающая скобка '('"),
            ')': (15, "закрывающая скобка ')'"),
            ',': (16, "запятая"),
            '{': (17, "открывающая фигурная скобка '{'"),
            '}': (18, "закрывающая фигурная скобка '}'"),
            ';': (19, "конец оператора ';'")
        }

    def analyze(self, text):
        tokens = []
        i = 0
        line = 1
        col = 1

        while i < len(text):
            char = text[i]
            start_col = col

            if char in ' \t\n\r':
                if char == '\n':
                    tokens.append(Token(12, "разделитель (перенос)", "\\n", line, start_col, col))
                    line += 1
                    col = 1
                elif char == '\t':
                    tokens.append(Token(12, "разделитель (табуляция)", "\\t", line, start_col, col))
                    col += 1
                elif char == '\r':
                    tokens.append(Token(12, "разделитель (возврат)", "\\r", line, start_col, col))
                    col += 1
                else:
                    tokens.append(Token(12, "разделитель (пробел)", "(пробел)", line, start_col, col))
                    col += 1
                i += 1
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
                tokens.append(Token(20, "целое без знака", lexeme, line, start_col, col - 1))
                continue

            if char == '-':
                if i + 1 < len(text) and text[i + 1] == '>':
                    tokens.append(Token(8, "оператор '->'", "->", line, start_col, col + 1))
                    i += 2
                    col += 2
                else:
                    tokens.append(Token(7, "оператор '-'", "-", line, start_col, col))
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