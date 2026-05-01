class SyntaxError:
    def __init__(self, message, line, column, lexeme):
        self.message = message
        self.line = line
        self.column = column
        self.lexeme = lexeme


class Parser:
    def __init__(self, tokens):
        self.tokens = [t for t in tokens if t.type_name != 'Space']
        self.pos = 0
        self.errors = []

        self.quads = []
        self.temp_count = 0

    def get_current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def match(self, expected_type=None, expected_value=None):
        token = self.get_current_token()
        if not token:
            return False

        if expected_type and token.type_name != expected_type:
            return False
        if expected_value and token.value != expected_value:
            return False

        self.pos += 1
        return True

    def error(self, message):
        token = self.get_current_token()
        if token:
            self.errors.append(SyntaxError(message, token.line, token.start, token.value))
        else:
            last_token = self.tokens[-1] if self.tokens else None
            line = last_token.line if last_token else 1
            col = last_token.end if last_token else 1
            self.errors.append(SyntaxError(message, line, col, "EOF"))

    def parse(self):
        if not self.tokens or (len(self.tokens) == 1 and self.tokens[0].type_name == 'EOF'):
            return []

        self.expression()

        token = self.get_current_token()
        if token and token.type_name != 'EOF':
            self.error("Лишние символы в конце выражения")

        return self.errors

    def expression(self):
        self.term()
        self.A()

    def A(self):
        token = self.get_current_token()
        if token and token.value in ('+', '-'):
            self.match()
            self.term()
            self.A()

    def term(self):
        self.factor()
        self.B()
    def B(self):
        token = self.get_current_token()
        if token and token.value in ('*', '/', '%'):
            self.match()
            self.factor()
            self.B()

    def factor(self):
        token = self.get_current_token()
        if not token:
            self.error("Ожидался операнд (число или идентификатор)")
            return

        if token.type_name == 'Number':
            self.match()
        elif token.type_name == 'Identifier':
            self.match()
        elif token.value == '(':
            self.match()
            self.expression()
            if not self.match(expected_value=')'):
                self.error("Пропущена закрывающая скобка ')'")
        else:
            self.error(f"Недопустимый символ в выражении: {token.value}")