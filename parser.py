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
        if not self.panic_mode:
            self.errors.append(ParseError(token, expected, message))
            self.panic_mode = True

    def irons_recover(self, expected, is_type, sync_tokens):
        sync_list = sync_tokens or []

        if self.pos < len(self.tokens):
            err_lexeme = self.tokens[self.pos].lexeme
            while self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].lexeme == err_lexeme:
                self.pos += 1

        temp_pos = self.pos
        while temp_pos < len(self.tokens):
            token = self.tokens[temp_pos]
            is_exp = (is_type and token.type_name == expected) or (not is_type and token.lexeme == expected)
            is_sync = token.lexeme in sync_list or token.type_name in sync_list

            if is_exp or is_sync:
                self.pos = temp_pos
                return True
            temp_pos += 1

        return False

    def match(self, expected, is_type=False, sync_tokens=None):
        token = self.current_token()

        if token is None:
            self.add_error(None, expected)
            raise StopParsing()

        is_matched = (is_type and token.type_name == expected) or (not is_type and token.lexeme == expected)
        if is_matched:
            self.advance()
            self.panic_mode = False
            return True

        self.add_error(token, expected)

        if not self.irons_recover(expected, is_type, sync_tokens):
            raise StopParsing()

        curr = self.current_token()
        if curr:
            is_exp = (is_type and curr.type_name == expected) or (not is_type and curr.lexeme == expected)
            if is_exp:
                self.advance()
                self.panic_mode = False

        return True

    def parse(self):
        if not self.tokens:
            return self.errors

        while self.pos < len(self.tokens):
            try:
                self.parse_start()
            except StopParsing:
                self.recover_to_next_statement()

        return self.errors

    def recover_to_next_statement(self):
        if self.pos < len(self.tokens):
            self.pos += 1
        self.panic_mode = False

    def parse_start(self):
        self.match("let", sync_tokens=["идентификатор", "=", "{"])
        self.match("идентификатор", is_type=True, sync_tokens=["=", "{", "("])
        self.match("=", sync_tokens=["{", "("])
        self.match("{", sync_tokens=["(", "идентификатор"])
        self.match("(", sync_tokens=["идентификатор", ")", "->"])

        if self.current_token() and self.current_token().lexeme != ")":
            self.parse_param_list()

        self.match(")", sync_tokens=["->", "in"])
        self.match("->", sync_tokens=["Int", "String", "Float", "Bool", "in"])
        self.parse_type()
        self.match("in", sync_tokens=["return", "идентификатор", "константа", "("])
        self.match("return", sync_tokens=["идентификатор", "константа", "(", "}"])

        self.parse_expr()

        self.match("}", sync_tokens=[";", "let"])
        self.match(";", sync_tokens=["let"])
        self.panic_mode = False

    def parse_param_list(self):
        self.parse_param()
        while self.current_token() and self.current_token().lexeme == ",":
            self.match(",")
            if self.current_token() and self.current_token().lexeme != ")":
                self.parse_param()

    def parse_param(self):
        if not self.current_token() or self.current_token().lexeme in [")", "->", "in"]:
            return

        self.match("идентификатор", is_type=True, sync_tokens=[":", ",", ")", "->"])
        self.match(":", sync_tokens=["Int", "String", "Float", "Bool", ",", ")"])
        self.parse_type()

    def parse_type(self):
        token = self.current_token()
        if not token:
            self.add_error(None, "Тип данных")
            raise StopParsing()

        types = ["Int", "String", "Float", "Bool"]
        if token.lexeme in types:
            self.advance()
            self.panic_mode = False
            return True

        self.add_error(token, "Тип данных (Int, String, Float, Bool)")

        sync_list = types + [")", "in", ",", "return", "}", ";"]
        if not self.irons_recover("Int", False, sync_list):
            raise StopParsing()

        curr = self.current_token()
        if curr and curr.lexeme in types:
            self.advance()
            self.panic_mode = False
        return True

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
            if not self.irons_recover("идентификатор", True, ["}", ")", "return", ";"]):
                raise StopParsing()

            curr = self.current_token()
            if curr and curr.type_name in ["идентификатор", "константа"]:
                self.advance()
                self.panic_mode = False
            elif curr and curr.lexeme == "(":
                self.advance()
                self.panic_mode = False
                self.parse_expr()
                self.match(")", sync_tokens=["+", "-", "*", "/", "}", ";"])