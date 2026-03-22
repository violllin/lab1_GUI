class ParseError:
    def __init__(self, token, expected, message=""):
        self.token = token
        self.expected = expected
        if message:
            self.message = message
        else:
            lexeme = token.lexeme if token else "конец файла"
            self.message = f"Ожидалось '{expected}', получено '{lexeme}'"

class Parser:

    def __init__(self, tokens):
        self.tokens = [t for t in tokens if t.code != 14]
        self.pos = 0
        self.errors = []

    def current_token(self):
        while self.pos < len(self.tokens) and self.tokens[self.pos].is_error:
            bad_token = self.tokens[self.pos]
            self.errors.append(ParseError(bad_token, "правильный символ", f"Недопустимый символ: '{bad_token.lexeme}'"))
            self.pos += 1

        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self):
        self.pos += 1

    def irons_recover(self, expected, is_type, sync_tokens, error_token=None):
        sync_list = sync_tokens or []

        while self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            is_exp = (is_type and token.type_name == expected) or (not is_type and token.lexeme == expected)
            is_sync = token.lexeme in sync_list or token.type_name in sync_list

            if is_exp or is_sync:
                break

            if token != error_token:
                self.errors.append(ParseError(token, expected, f"Лишний символ: '{token.lexeme}'"))
            self.pos += 1

        token = self.current_token()
        if token:
            is_exp = (is_type and token.type_name == expected) or (not is_type and token.lexeme == expected)
            if is_exp:
                self.pos += 1
            else:
                pass
            return True
        return False

    def match(self, expected, is_type=False, sync_tokens=None):
        token = self.current_token()

        if token and ((is_type and token.type_name == expected) or (not is_type and token.lexeme == expected)):
            self.advance()
            return True

        if token and not is_type and expected in ["let", "return", "in"]:
            next_t = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
            if next_t:
                is_typo = False
                if expected == "let" and next_t.type_name == "идентификатор":
                    is_typo = True
                elif expected == "return" and (
                        next_t.type_name in ["идентификатор", "константа"] or next_t.lexeme == "("):
                    is_typo = True
                elif expected == "in" and next_t.lexeme == "return":
                    is_typo = True

                if is_typo:
                    self.errors.append(ParseError(token, expected))
                    self.advance()
                    return True

        self.errors.append(ParseError(token, expected))
        return self.irons_recover(expected, is_type, sync_tokens, error_token=token)

    def recover(self, sync_tokens):
        while self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            if token.lexeme in sync_tokens or token.type_name in sync_tokens:
                break
            self.pos += 1

    def parse(self):
        self.parse_start()

        while self.current_token() is not None:
            token = self.current_token()
            self.errors.append(ParseError(token, "конец файла", f"Лишний символ в конце файла: '{token.lexeme}'"))
            self.advance()

        return self.errors

    def parse_start(self):
        self.match("let", sync_tokens=["идентификатор", "=", "{"])
        self.match("идентификатор", is_type=True, sync_tokens=["=", "{"])
        self.match("=", sync_tokens=["{"])
        self.match("{", sync_tokens=["("])
        self.match("(", sync_tokens=["идентификатор", ")", "->"])

        if self.current_token() and self.current_token().lexeme != ")":
            self.parse_param_list()

        self.match(")", sync_tokens=["->", "in"])
        self.match("->", sync_tokens=["Int", "String", "Float", "Bool", "in", "return", "идентификатор", "константа", "("])
        self.parse_type()
        self.match("in", sync_tokens=["return", "идентификатор", "константа", "("])
        self.match("return", sync_tokens=["идентификатор", "константа", "("])

        self.parse_expr()

        self.match("}", sync_tokens=[";"])
        self.match(";")

    def parse_param_list(self):
        self.parse_param()
        while self.current_token() and self.current_token().lexeme == ",":
            self.advance()

            while self.current_token() and self.current_token().lexeme == ",":
                self.errors.append(ParseError(self.current_token(), "идентификатор", f"Лишняя запятая"))
                self.advance()

            if self.current_token() and self.current_token().lexeme == ")":
                self.errors.append(ParseError(self.current_token(), "идентификатор"))
                break

            self.parse_param()

    def parse_param(self):
        self.match("идентификатор", is_type=True, sync_tokens=[":", ",", ")"])
        self.match(":", sync_tokens=["Int", "String", "Float", "Bool", ",", ")"])
        self.parse_type()

    def parse_type(self):
        token = self.current_token()
        if not token:
            self.errors.append(ParseError(None, "Тип данных (Int, String, Float, Bool)"))
            return False

        types = ["Int", "String", "Float", "Bool"]
        if token.lexeme in types:
            self.advance()
            return True

        self.errors.append(ParseError(token, "Тип данных (Int, String, Float, Bool)"))

        sync_tokens = [",", ")", "in", "{"]

        return self.irons_recover("Int", False, sync_tokens, error_token=token)

    def parse_expr(self):
        self.parse_term()
        while self.current_token() and self.current_token().lexeme in ["+", "-"]:
            self.advance()
            self.parse_term()

    def parse_term(self):
        self.parse_factor()
        while self.current_token() and self.current_token().lexeme in ["*", "/", "%"]:
            self.advance()
            self.parse_factor()

    def parse_factor(self):
        token = self.current_token()
        if not token: return

        if token.type_name in ["идентификатор", "константа"]:
            self.advance()
        elif token.lexeme == "(":
            self.advance()
            self.parse_expr()
            self.match(")", sync_tokens=["+", "-", "*", "/", "}", ";"])
        else:
            self.errors.append(ParseError(token, "Выражение"))
            self.irons_recover("идентификатор", True, ["+", "-", "*", "/", "}", ";", ")", "return"], error_token=token)