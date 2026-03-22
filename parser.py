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

    def match(self, expected, is_type=False, sync_tokens=None):
        token = self.current_token()
        if not token:
            self.errors.append(ParseError(None, expected))
            return False

        if (is_type and token.type_name == expected) or (not is_type and token.lexeme == expected):
            self.advance()
            return True

        self.errors.append(ParseError(token, expected))
        sync_list = sync_tokens or []

        if not is_type and token.type_name == "идентификатор":
            if expected == "let" and self.pos + 1 < len(self.tokens):
                next_t = self.tokens[self.pos + 1]
                if next_t.type_name == "идентификатор":
                    self.pos += 1
                    return True
            elif expected == "return" and self.pos + 1 < len(self.tokens):
                next_t = self.tokens[self.pos + 1]
                if next_t.type_name in ["идентификатор", "константа"] or next_t.lexeme == "(":
                    self.pos += 1
                    return True

        if token.lexeme in sync_list or token.type_name in sync_list:
            return False

        temp_pos = self.pos
        found_expected = False
        found_sync = False

        while temp_pos < len(self.tokens):
            t = self.tokens[temp_pos]
            if (is_type and t.type_name == expected) or (not is_type and t.lexeme == expected):
                found_expected = True
                break
            if t.lexeme in sync_list or t.type_name in sync_list:
                found_sync = True
                break
            temp_pos += 1

        for i in range(self.pos + 1, temp_pos):
            self.errors.append(ParseError(self.tokens[i], expected, f"Лишний символ: '{self.tokens[i].lexeme}'"))

        if found_expected:
            self.pos = temp_pos + 1
            return True
        else:
            self.pos = temp_pos
            return False

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
        self.match("->", sync_tokens=["Int", "String", "Float", "Bool", "in"])
        self.parse_type()
        self.match("in", sync_tokens=["return"])
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
        sync_tokens = [",", ")", "in", "->", "return", "{", "}", ";"]

        if token.lexeme in sync_tokens or token.type_name in sync_tokens:
            return False

        temp_pos = self.pos
        found_expected = False

        while temp_pos < len(self.tokens):
            t = self.tokens[temp_pos]
            if t.lexeme in types:
                found_expected = True
                break
            if t.lexeme in sync_tokens or t.type_name in sync_tokens:
                break
            temp_pos += 1

        for i in range(self.pos + 1, temp_pos):
            self.errors.append(ParseError(self.tokens[i], "Тип данных", f"Лишний символ: '{self.tokens[i].lexeme}'"))

        if found_expected:
            self.pos = temp_pos + 1
            return True
        else:
            self.pos = temp_pos
            return False

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
            self.recover(["+", "-", "*", "/", "}", ";", ")", "return"])