class AppSyntaxError:
    def __init__(self, message, line, column, lexeme):
        self.message = message
        self.line = line
        self.column = column
        self.lexeme = lexeme

class Quadruple:
    def __init__(self, op, arg1, arg2, result):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result


class Parser:
    def __init__(self, tokens):
        self.tokens = [t for t in tokens if t.type_name != 'Space']
        self.pos = 0
        self.errors = []

        self.quadruples = []
        self.temp_counter = 1

    def new_temp(self):
        name = f"t{self.temp_counter}"
        self.temp_counter += 1
        return name

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
            return [], []

        while self.pos < len(self.tokens):
            token = self.get_current_token()
            if not token or token.type_name == 'EOF':
                break

            if token.type_name in ('Number', 'Identifier') or token.value in ('(', '+', '-'):
                self.expression()
            else:
                self.error(f"Недопустимый символ: {token.value}")
                self.pos += 1

        if self.errors:
            self.quadruples = []

        return self.errors, self.quadruples

    def expression(self):
        left = self.term()
        while True:
            token = self.get_current_token()
            if token and token.value in ('+', '-'):
                op = token.value
                self.match()
                right = self.term()
                if not self.errors:
                    res = self.new_temp()
                    self.quadruples.append((op, left, right, res))
                    left = res
            else:
                break
        return left

    def term(self):
        left = self.factor()
        while True:
            token = self.get_current_token()
            if token and token.value in ('*', '/', '%'):
                op = token.value
                self.match()
                right = self.factor()
                if not self.errors:
                    res = self.new_temp()
                    self.quadruples.append((op, left, right, res))
                    left = res
            else:
                break
        return left

    def factor(self):
        token = self.get_current_token()
        if not token or token.type_name == 'EOF':
            self.error("Ожидался операнд")
            return None

        if token.value in ('+', '-'):
            op = token.value
            self.match()
            operand = self.factor()
            if not self.errors:
                res = self.new_temp()
                self.quadruples.append(Quadruple(op, operand, "—", res))
                return res
            return None

        if token.type_name in ('Number', 'Identifier'):
            val = token.value
            self.match()
            return val

        elif token.value == '(':
            self.match()
            val = self.expression()
            if not self.match(expected_value=')'):
                self.error("Пропущена ')'")
            return val

        else:
            self.error(f"Некорректный фактор: {token.value}")
            self.pos += 1
            return None