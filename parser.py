class ParseError:
    def __init__(self, token, expected, message=""):
        self.token = token
        self.expected = expected
        if message:
            self.message = message
        else:
            lexeme = token.lexeme if token else "конец файла"
            self.message = f"Ожидалось '{expected}', получено '{lexeme}'"


class StopParsing(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = [t for t in tokens if t.code != 14]
        self.pos = 0
        self.errors = []
        self.panic_mode = False

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self):
        self.pos += 1

    def add_error(self, token, expected, message=""):
        if self.panic_mode:
            return

        current_pos = (token.line, token.start) if token else (0, 0)

        if not self.errors or (self.errors[-1].token.line, self.errors[-1].token.start) != current_pos:
            self.errors.append(ParseError(token, expected, message))

        self.panic_mode = True

    def irons_recover(self, expected, is_type, sync_tokens):
        sync_list = sync_tokens or []

        while self.pos < len(self.tokens):
            token = self.tokens[self.pos]

            is_matched = (is_type and token.type_name == expected) or \
                         (not is_type and token.lexeme == expected)

            if is_matched or token.lexeme in sync_list or token.type_name in sync_list:
                return True

            self.advance()

        return False

    def match(self, expected, is_type=False, sync_tokens=None):
        token = self.current_token()

        if token is None:
            self.add_error(None, expected)
            raise StopParsing()

        is_matched = (is_type and token.type_name == expected) or \
                     (not is_type and token.lexeme == expected)

        if is_matched:
            self.advance()
            self.panic_mode = False
            return True

        self.add_error(token, expected)

        if not self.irons_recover(expected, is_type, sync_tokens):
            raise StopParsing()

        curr = self.current_token()
        if curr:
            is_exp = (is_type and curr.type_name == expected) or \
                     (not is_type and curr.lexeme == expected)
            if is_exp:
                self.advance()
                self.panic_mode = False

        return True

    def parse(self):
        if not self.tokens:
            return self.errors

        try:
            self.parse_start()
        except StopParsing:
            pass

        return self.errors

    def parse_start(self):
        # let <id> = {
        self.match("let", sync_tokens=["="])
        self.match("идентификатор", is_type=True, sync_tokens=["="])
        self.match("=", sync_tokens=["{"])
        self.match("{", sync_tokens=["("])

        self.parse_lambda_body()

        self.match("}", sync_tokens=[";"])
        self.match(";", sync_tokens=[])

    def parse_lambda_body(self):
        self.match("(", sync_tokens=[")", "->"])

        if self.current_token() and self.current_token().lexeme != ")":
            self.parse_params()

        self.match(")", sync_tokens=["->"])
        self.match("->", sync_tokens=["Int", "String", "Bool", "Float", "in"])
        self.parse_type()
        self.match("in", sync_tokens=["return"])
        self.match("return", sync_tokens=["+", "-", "(", "идентификатор", "константа"])

        self.parse_expr()

    def parse_params(self):
        self.parse_param()
        while self.current_token() and self.current_token().lexeme == ",":
            self.advance()
            self.parse_param()

    def parse_param(self):
        self.match("идентификатор", is_type=True, sync_tokens=[":", ",", ")"])
        self.match(":", sync_tokens=["Int", "String", "Bool", "Float", ",", ")"])
        self.parse_type()

    def parse_type(self):
        token = self.current_token()
        types = ["Int", "String", "Bool", "Float"]
        if token and token.lexeme in types:
            self.advance()
            self.panic_mode = False
        else:
            self.add_error(token, "Тип данных (Int, String...)")
            if not self.irons_recover("", False, [",", ")", "->", "in", "return", "идентификатор"]):
                raise StopParsing()

    def parse_expr(self):
        self.parse_term()
        while self.current_token() and self.current_token().lexeme in ["+", "-"]:
            self.match(self.current_token().lexeme)
            self.parse_term()

    def parse_term(self):
        self.parse_factor()
        while self.current_token() and self.current_token().lexeme in ["*", "/", "%"]:
            self.match(self.current_token().lexeme)
            self.parse_factor()

    def parse_factor(self):
        token = self.current_token()
        if not token:
            self.add_error(None, "Выражение")
            return

        if token.type_name in ["идентификатор", "константа"]:
            self.advance()
            self.panic_mode = False
        elif token.lexeme == "(":
            self.advance()
            self.panic_mode = False
            self.parse_expr()
            self.match(")", sync_tokens=["+", "-", "*", "/", "}", ";"])
        else:
            self.add_error(token, "Выражение")
            if not self.irons_recover("идентификатор", True, ["константа", "(", "}", ")", "return", ";"]):
                raise StopParsing()

            curr = self.current_token()
            if curr:
                if curr.lexeme == "(":
                    self.advance()
                    self.parse_expr()
                    self.match(")")
                    self.panic_mode = False
                elif curr.type_name in ["идентификатор", "константа"]:
                    self.advance()
                    self.panic_mode = False