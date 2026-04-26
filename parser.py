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

    def peek(self, distance=1):
        if self.pos + distance < len(self.tokens):
            return self.tokens[self.pos + distance]
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

    def skip_corrupted_word(self, failed_token, expected):
        self.advance()

        is_keyword = expected in ["let", "in", "return", "Int", "String", "Float", "Bool"]

        while self.current_token():
            curr = self.tokens[self.pos]
            prev = self.tokens[self.pos - 1]

            if curr.lexeme == failed_token.lexeme:
                self.advance()
                continue

            if prev.line == curr.line and curr.start <= prev.end + 1:
                if curr.lexeme in ["{", "}", "(", ")", ";", ",", ":"] and curr.lexeme != failed_token.lexeme:
                    break

                is_curr_error = getattr(curr, 'is_error', False) or curr.type_name == "недопустимый символ"
                is_failed_error = getattr(failed_token, 'is_error',
                                          False) or failed_token.type_name == "недопустимый символ"
                is_prev_error = getattr(prev, 'is_error', False) or prev.type_name == "недопустимый символ"

                if is_curr_error or is_failed_error:
                    self.advance()
                elif is_prev_error and curr.type_name in ["идентификатор", "константа", "ключевое слово"]:
                    self.advance()
                elif is_keyword:
                    self.advance()
                else:
                    break
            else:
                break

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

        if is_matched and expected == "идентификатор":
            temp_pos = self.pos
            has_error_attached = False
            while temp_pos + 1 < len(self.tokens):
                curr = self.tokens[temp_pos]
                nxt = self.tokens[temp_pos + 1]
                if curr.line == nxt.line and nxt.start <= curr.end + 1:
                    if nxt.lexeme in ["{", "}", "(", ")", ";", ",", ":"]:
                        break
                    if getattr(nxt, 'is_error', False) or nxt.type_name == "недопустимый символ" or nxt.lexeme in ["?",
                                                                                                                   "@",
                                                                                                                   "!",
                                                                                                                   "%",
                                                                                                                   "^",
                                                                                                                   "&",
                                                                                                                   "*"]:
                        has_error_attached = True
                        break
                    temp_pos += 1
                else:
                    break

            if has_error_attached:
                is_matched = False

        if is_matched:
            self.advance()
            self.panic_mode = False
            return True

        if expected == "->" and token.lexeme in ["-", ">", "="]:
            self.add_error(token, "->")
            self.skip_corrupted_word(token, expected)
            self.panic_mode = False
            return True

        keywords = ["let", "in", "return", "Int", "String", "Float", "Bool"]
        if not is_matched and not is_type and expected in keywords and token.type_name == "идентификатор":
            self.add_error(token, expected)
            self.skip_corrupted_word(token, expected)
            self.panic_mode = False
            return True

        self.add_error(token, expected)
        self.skip_corrupted_word(token, expected)

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
        self.match("->", sync_tokens=["Int", "String", "Bool", "Float", "in"])
        self.parse_type()
        self.match("in", sync_tokens=["return"])
        self.match("return", sync_tokens=["+", "-", "(", "идентификатор", "константа"])
        self.parse_expr()

    def parse_params(self):
        while self.current_token():
            self.parse_param()

            token = self.current_token()
            if not token or token.lexeme == "->":
                break

            if token.lexeme == ")":
                break

            if token.lexeme == ",":
                self.advance()
                next_t = self.current_token()
                if next_t and next_t.lexeme == ")":
                    self.add_error(next_t, "идентификатор")
            elif token.type_name == "идентификатор":
                self.add_error(token, ",")
                continue
            else:
                if not self.irons_recover(",", False, [")", "->"]):
                    break

    def parse_param(self):
        self.match("идентификатор", is_type=True, sync_tokens=[":", ",", "->"])
        self.match(":", sync_tokens=["Int", "String", "Bool", "Float", ",", "->"])
        self.parse_type()

    def parse_type(self):
        token = self.current_token()
        types = ["Int", "String", "Bool", "Float"]
        if token and token.lexeme in types:
            self.advance()
            self.panic_mode = False
        else:
            self.add_error(token, "Тип данных (Int, String, Float, Bool)")
            self.skip_corrupted_word(token, "Тип данных")
            if not self.irons_recover("", False, [",", "in", "->", ")"]):
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

        if token.type_name == "идентификатор":
            self.match("идентификатор", is_type=True, sync_tokens=["+", "-", "*", "/", "}", ")", ";"])
        elif token.type_name == "константа":
            self.match("константа", is_type=True, sync_tokens=["+", "-", "*", "/", "}", ")", ";"])
        elif token.lexeme == "(":
            self.match("(")
            self.parse_expr()
            self.match(")", sync_tokens=["+", "-", "*", "/", "}", ";"])
        else:
            self.add_error(token, "Выражение")
            self.skip_corrupted_word(token, "Выражение")
            if not self.irons_recover("идентификатор", True,
                                      ["константа", "(", "}", ")", ";", "+", "-", "*", "/", "%"]):
                raise StopParsing()