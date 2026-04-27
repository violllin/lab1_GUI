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
            return token.lexeme in ["Int", "String", "Bool", "Float", "Double"]
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
            self.advance()
            self.panic_mode = False
            return True

        sync_list = sync_tokens or []

        if token.lexeme in sync_list or token.type_name in sync_list:
            self.add_error(token, expected)
            return True

        skipped_tokens = [token]
        self.advance()

        while self.pos < len(self.tokens):
            curr = self.tokens[self.pos]
            last_skipped = skipped_tokens[-1]

            is_touching = (curr.line == last_skipped.line and curr.start <= last_skipped.end + 1)
            is_same_lexeme = (curr.lexeme == last_skipped.lexeme)

            if is_touching or is_same_lexeme:
                if curr.lexeme in sync_list or curr.type_name in sync_list:
                    break
                skipped_tokens.append(curr)
                self.advance()
            else:
                break

        bad_fragment = "".join(t.lexeme for t in skipped_tokens)
        err_token = type(token)(token.code, token.type_name, bad_fragment,
                                skipped_tokens[0].line, skipped_tokens[0].start,
                                skipped_tokens[-1].end)

        self.add_error(err_token, expected)

        curr = self.current_token()
        if curr and self.check_match(curr, expected, is_type):
            self.advance()
            self.panic_mode = False

        return True

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
        self.match("let", sync_tokens=["идентификатор"])
        self.match("идентификатор", is_type=True, sync_tokens=["="])
        self.match("=", sync_tokens=["{"])
        self.match("{", sync_tokens=["("])
        self.parse_lambda_body()
        self.match("}", sync_tokens=[";"])
        self.match(";", sync_tokens=["let"])

    def parse_lambda_body(self):
        self.match("(", sync_tokens=["идентификатор", ")"])

        curr = self.current_token()
        if curr and curr.lexeme != ")":
            self.parse_params()

        self.match(")", sync_tokens=["->"])
        self.match("->", sync_tokens=["Тип данных (Int, String, Float, Bool)"])
        self.parse_type()
        self.match("in", sync_tokens=["return"])
        self.match("return", sync_tokens=["идентификатор", "константа", "(", "Выражение"])
        self.parse_expr()

    def parse_params(self):
        while self.current_token():
            token = self.current_token()
            if token.lexeme == ")":
                break

            self.parse_param()

            token = self.current_token()
            if not token or token.lexeme in ["->", ")"]:
                break

            if token.lexeme == ",":
                comma_token = token
                self.match(",")

                if self.current_token() and self.current_token().lexeme == ",":
                    err_tokens = []
                    while self.current_token() and self.current_token().lexeme == ",":
                        err_tokens.append(self.current_token())
                        self.advance()

                    bad_fragment = "".join(t.lexeme for t in err_tokens)
                    err_token = type(token)(token.code, token.type_name, bad_fragment,
                                            err_tokens[0].line, err_tokens[0].start,
                                            err_tokens[-1].end)
                    self.add_error(err_token, "идентификатор", f"Лишние символы: '{bad_fragment}'")

                if self.current_token() and self.current_token().lexeme == ")":
                    self.add_error(comma_token, "параметр", "Ожидался параметр после запятой")
                    break
            else:
                if not self.panic_mode:
                    self.add_error(token, ",")
                    self.panic_mode = True
                self.advance()

    def parse_param(self):
        self.match("идентификатор", is_type=True, sync_tokens=[":"])
        self.match(":", sync_tokens=["Тип данных (Int, String, Float, Bool)"])
        self.parse_type()

    def parse_type(self):
        self.match("Тип данных (Int, String, Float, Bool)", sync_tokens=[",", ")", "in", "->"])

    def parse_expr(self):
        self.parse_term()
        while self.current_token():
            curr = self.current_token()
            if curr.lexeme in ["+", "-"]:
                self.match(curr.lexeme)
                self.parse_term()
            elif curr.lexeme in ["*", "/", "%", ")", "}", ";", ",", "in", "return", "->", "=", "{", ":"]:
                break
            else:
                err_tokens = [curr]
                self.advance()
                while self.current_token():
                    next_tok = self.current_token()
                    last_tok = err_tokens[-1]
                    is_touching = (next_tok.line == last_tok.line and next_tok.start <= last_tok.end + 1)
                    is_same = (next_tok.lexeme == last_tok.lexeme)
                    if is_touching or is_same:
                        if next_tok.lexeme in ["+", "-", "*", "/", "%", ")", "}", ";", ",", "in", "return", "->", "=",
                                               "{", ":"]:
                            break
                        err_tokens.append(next_tok)
                        self.advance()
                    else:
                        break
                bad_fragment = "".join(t.lexeme for t in err_tokens)
                err_token = type(err_tokens[0])(err_tokens[0].code, err_tokens[0].type_name, bad_fragment,
                                                err_tokens[0].line, err_tokens[0].start,
                                                err_tokens[-1].end)
                self.add_error(err_token, "Выражение", f"Неожиданный символ в выражении: '{bad_fragment}'")

    def parse_term(self):
        self.parse_factor()
        while self.current_token():
            curr = self.current_token()
            if curr.lexeme in ["*", "/", "%"]:
                self.match(curr.lexeme)
                self.parse_factor()
            elif curr.lexeme in ["+", "-", ")", "}", ";", ",", "in", "return", "->", "=", "{", ":"]:
                break
            else:
                err_tokens = [curr]
                self.advance()
                while self.current_token():
                    next_tok = self.current_token()
                    last_tok = err_tokens[-1]
                    is_touching = (next_tok.line == last_tok.line and next_tok.start <= last_tok.end + 1)
                    is_same = (next_tok.lexeme == last_tok.lexeme)
                    if is_touching or is_same:
                        if next_tok.lexeme in ["+", "-", "*", "/", "%", ")", "}", ";", ",", "in", "return", "->", "=",
                                               "{", ":"]:
                            break
                        err_tokens.append(next_tok)
                        self.advance()
                    else:
                        break
                bad_fragment = "".join(t.lexeme for t in err_tokens)
                err_token = type(err_tokens[0])(err_tokens[0].code, err_tokens[0].type_name, bad_fragment,
                                                err_tokens[0].line, err_tokens[0].start,
                                                err_tokens[-1].end)
                self.add_error(err_token, "Выражение", f"Неожиданный символ в выражении: '{bad_fragment}'")

    def parse_factor(self):
        token = self.current_token()
        if not token:
            self.add_error(None, "Выражение")
            return

        if token.type_name == "идентификатор":
            self.match("идентификатор", is_type=True, sync_tokens=["+", "-", "*", "/", "%", "}", ")", ";", ","])
        elif token.type_name == "константа":
            self.match("константа", is_type=True, sync_tokens=["+", "-", "*", "/", "%", "}", ")", ";", ","])
        elif token.lexeme == "(":
            self.match("(", sync_tokens=["идентификатор", "константа", "Выражение"])
            self.parse_expr()
            self.match(")", sync_tokens=["+", "-", "*", "/", "%", "}", ";", ","])
        else:
            self.match("Выражение", sync_tokens=["+", "-", "*", "/", "%", "}", ")", ";", ","])