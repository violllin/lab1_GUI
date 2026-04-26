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

    def check_match(self, token, expected, is_type):
        if expected.startswith("Тип данных"):
            return token.lexeme in ["Int", "String", "Bool", "Float"]
        if expected == "Выражение":
            return token.type_name in ["идентификатор", "константа"] or token.lexeme == "("
        return (is_type and token.type_name == expected) or \
            (not is_type and token.lexeme == expected)

    def match(self, expected, is_type=False, sync_tokens=None):
        token = self.current_token()

        if not token:
            self.add_error(None, expected)
            raise StopParsing()

        if self.check_match(token, expected, is_type):
            if expected == "идентификатор" or expected == "->":
                contiguous = [token]
                pos = self.pos + 1
                has_garbage = False
                while pos < len(self.tokens):
                    prev = self.tokens[pos - 1]
                    curr = self.tokens[pos]
                    # Проверяем, идут ли символы слитно
                    if prev.line == curr.line and curr.start <= prev.end + 1:
                        if expected == "->" and curr.lexeme in ["Int", "String", "Float", "Bool"]:
                            break
                        if expected == "идентификатор" and curr.lexeme in set("(){}:;,+-*/%="):
                            break
                        contiguous.append(curr)
                        has_garbage = True
                        pos += 1
                    else:
                        break

                if has_garbage:
                    bad_fragment = "".join(t.lexeme for t in contiguous)
                    err_token = type(token)(token.code, token.type_name, bad_fragment, token.line, token.start,
                                            contiguous[-1].end)
                    self.add_error(err_token, expected)
                    self.pos = pos
                    self.panic_mode = False
                    return True

            self.advance()
            self.panic_mode = False
            return True

        contiguous = [token]
        pos = self.pos
        structural = set("(){}:;,+-*/%=")

        while pos + 1 < len(self.tokens):
            c_t = self.tokens[pos]
            n_t = self.tokens[pos + 1]

            if c_t.line == n_t.line and n_t.start <= c_t.end + 1:
                if self.check_match(n_t, expected, is_type):
                    break
                if is_type and expected == "идентификатор":
                    if n_t.lexeme in structural and n_t.lexeme != c_t.lexeme:
                        break
                contiguous.append(n_t)
                pos += 1
            else:
                break

        bad_fragment = "".join(t.lexeme for t in contiguous)
        err_token = type(token)(token.code, token.type_name, bad_fragment, token.line, token.start, contiguous[-1].end)

        self.add_error(err_token, expected)
        self.pos += len(contiguous)
        self.panic_mode = True

        sync_list = sync_tokens or []
        while self.pos < len(self.tokens):
            curr = self.tokens[self.pos]

            if self.check_match(curr, expected, is_type):
                self.advance()
                self.panic_mode = False
                return True

            if curr.lexeme in sync_list or curr.type_name in sync_list:
                self.panic_mode = False
                return True

            self.advance()

        raise StopParsing()

    def parse(self):
        if not self.tokens:
            return self.errors

        while self.pos < len(self.tokens):
            try:
                self.parse_statement()
            except StopParsing:
                while self.pos < len(self.tokens) and self.current_token().lexeme != "let":
                    self.advance()
                self.panic_mode = False

        return self.errors

    def parse_statement(self):
        self.match("let", sync_tokens=["идентификатор", "="])
        self.match("идентификатор", is_type=True, sync_tokens=["="])
        self.match("=", sync_tokens=["{"])
        self.match("{", sync_tokens=["("])
        self.parse_lambda_body()
        self.match("}", sync_tokens=[";"])
        self.match(";", sync_tokens=["let"])

    def parse_lambda_body(self):
        self.match("(", sync_tokens=[")", "->"])

        curr = self.current_token()
        if curr and curr.lexeme != ")":
            self.parse_params()

        self.match(")", sync_tokens=["->"])
        self.match("->", sync_tokens=["Тип данных (Int, String, Float, Bool)", "Int", "String", "Bool", "Float", "in"])
        self.parse_type()
        self.match("in", sync_tokens=["return"])
        self.match("return", sync_tokens=["+", "-", "(", "идентификатор", "константа", "Выражение"])
        self.parse_expr()

    def parse_params(self):
        while self.current_token():
            token = self.current_token()
            if token.lexeme == ")":
                break

            self.parse_param()

            token = self.current_token()
            if not token or token.lexeme == "->":
                break
            if token.lexeme == ")":
                break

            if token.lexeme == ",":
                comma_token = token
                self.match(",")
                if self.current_token() and self.current_token().lexeme == ")":
                    self.add_error(comma_token, "параметр", "Ожидался параметр после запятой")
                    break
            else:
                if not self.panic_mode:
                    self.add_error(token, ",")
                break

    def parse_param(self):
        self.match("идентификатор", is_type=True, sync_tokens=[":", ",", "->"])
        self.match(":",
                   sync_tokens=["Тип данных (Int, String, Float, Bool)", "Int", "String", "Bool", "Float", ",", "->"])
        self.parse_type()

    def parse_type(self):
        self.match("Тип данных (Int, String, Float, Bool)", sync_tokens=[",", "in", "->", ")"])

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

        if token.type_name == "идентификатор":
            self.match("идентификатор", is_type=True, sync_tokens=["+", "-", "*", "/", "}", ")", ";"])
        elif token.type_name == "константа":
            self.match("константа", is_type=True, sync_tokens=["+", "-", "*", "/", "}", ")", ";"])
        elif token.lexeme == "(":
            self.match("(")
            self.parse_expr()
            self.match(")", sync_tokens=["+", "-", "*", "/", "}", ";"])
        else:
            self.match("Выражение", sync_tokens=["+", "-", "*", "/", "}", ")", ";"])