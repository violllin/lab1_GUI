class AppSyntaxError:
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

    def get_current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def match(self, expected_type=None, expected_value=None):
        token = self.get_current_token()
        if not token or token.type_name == 'EOF':
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
            self.errors.append(AppSyntaxError(message, token.line, token.start, token.value))
        else:
            last_token = self.tokens[-1] if self.tokens else None
            line = last_token.line if last_token else 1
            col = last_token.end if last_token else 1
            self.errors.append(AppSyntaxError(message, line, col, "EOF"))

    def parse(self):
        if not self.tokens:
            return []

        while self.pos < len(self.tokens):
            token = self.get_current_token()
            if not token or token.type_name == 'EOF':
                break

            if token.type_name in ('Number', 'Identifier') or token.value in ('(', '+', '-'):
                self.expression()
            else:
                self.error(f"Недопустимый символ: {token.value}")
                self.pos += 1
        return self.errors

    def expression(self):
        self.term()
        while True:
            token = self.get_current_token()
            if token and token.value in ('+', '-'):
                self.match()
                self.term()
            else:
                break

    def term(self):
        self.factor()
        while True:
            token = self.get_current_token()
            if token and token.value in ('*', '/', '%'):
                self.match()
                self.factor()
            else:
                break

    def factor(self):
        token = self.get_current_token()
        if not token or token.type_name == 'EOF':
            self.error("Ожидался операнд")
            return

        if token.value in ('+', '-'):
            self.match()
            self.factor()
            return

        if token.type_name in ('Number', 'Identifier'):
            self.match()
        elif token.value == '(':
            self.match()
            self.expression()
            if not self.match(expected_value=')'):
                self.error("Пропущена ')'")
        else:
            self.error(f"Некорректный фактор: {token.value}")
            self.pos += 1