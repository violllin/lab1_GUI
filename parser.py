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
        while self.current_token():
            curr = self.tokens[self.pos]
            prev = self.tokens[self.pos - 1]
            if prev.line == curr.line and curr.start <= prev.end + 1:
                self.advance()
            else:
                break

    def irons_recover(self, expected, is_type, sync_tokens):
        sync_list = sync_tokens or []
        while self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            if self.check_match(token, expected, is_type) or token.lexeme in sync_list or token.type_name in sync_list:
                return True
            self.advance()
        return False

    def check_match(self, token, expected, is_type):
        if expected.startswith("Тип данных"):
            return token.lexeme in ["Int", "String", "Bool", "Float"]
        if expected == "Выражение":
            return token.type_name in ["идентификатор", "константа"] or token.lexeme == "("
        return (is_type and token.type_name == expected) or \
               (not is_type and token.lexeme == expected)

    def match(self, expected, is_type=False, sync_tokens=None):
        token = self.current_token()

        if token is None:
            self.add_error(None, expected)
            raise StopParsing()

        if self.check_match(token, expected, is_type):
            self.advance()
            self.panic_mode = False
            return True

        contiguous = [token]
        pos = self.pos
        while pos + 1 < len(self.tokens):
            c_t = self.tokens[pos]
            n_t = self.tokens[pos + 1]
            if c_t.line == n_t.line and n_t.start <= c_t.end + 1:
                contiguous.append(n_t)
                pos += 1
            else:
                break

        combined_str = "".join(t.lexeme for t in contiguous)

        keywords = ["let", "in", "return", "Int", "String", "Float", "Bool", "->"]
        if not is_type and (expected in keywords or expected.startswith("Тип данных")):
            target_keywords = ["Int", "String", "Float", "Bool"] if expected.startswith("Тип данных") else [expected]
            import re
            if expected == "->":
                stripped = re.sub(r'[^a-zA-Z0-9\->]', '', combined_str)
            else:
                stripped = re.sub(r'[^a-zA-Z]', '', combined_str)

            matched_kw = None
            for kw in target_keywords:
                if kw in stripped or stripped == kw:
                    matched_kw = kw
                    break
            if matched_kw:
                syn_token = type(token)(token.code, token.type_name, combined_str, token.line, token.start, contiguous[-1].end)
                self.add_error(syn_token, expected)
                self.pos += len(contiguous)
                self.panic_mode = False
                return True

        if is_type and expected == "идентификатор" and len(contiguous) > 1:
            valid_chars = set("():{},;")
            has_structural = any(t.lexeme in valid_chars for t in contiguous)
            if not has_structural:
                import re
                letters = re.sub(r'[^a-zA-Z0-9]', '', combined_str)
                if letters:
                    syn_token = type(token)(token.code, "идентификатор", combined_str, token.line, token.start, contiguous[-1].end)
                    self.add_error(syn_token, expected)
                    self.pos += len(contiguous)
                    self.panic_mode = False
                    return True

        found_expected_at = -1
        for lookahead in range(1, min(10, len(self.tokens) - self.pos)):
            nxt = self.tokens[self.pos + lookahead]
            if self.check_match(nxt, expected, is_type):
                found_expected_at = lookahead
                break
            if nxt.lexeme in ["let", "in", "return", "{", "}", ";", "->"] and expected not in ["let", "in", "return", "{", "}", ";", "->"]:
                break

        if found_expected_at != -1:
            extra_tokens = self.tokens[self.pos : self.pos + found_expected_at]
            extra_str = "".join(t.lexeme for t in extra_tokens)
            syn_token = type(token)(token.code, token.type_name, extra_str, token.line, extra_tokens[0].start, extra_tokens[-1].end)

            self.add_error(syn_token, expected)
            self.pos += found_expected_at
            self.panic_mode = False
            self.advance()
            return True

        if sync_tokens:
            if any(token.lexeme == s or token.type_name == s for s in sync_tokens):
                self.add_error(token, expected)
                self.panic_mode = False
                return True

        self.add_error(token, expected)
        self.skip_corrupted_word(token, expected)

        if not self.irons_recover(expected, is_type, sync_tokens):
            raise StopParsing()

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
            self.parse_param()

            token = self.current_token()
            if not token or token.lexeme == "->":
                break

            if token.lexeme == ")":
                break

            if token.lexeme == ",":
                self.match(",")
            else:
                if not self.irons_recover(",", False, [")", "->", "идентификатор"]):
                    break

    def parse_param(self):
        self.match("идентификатор", is_type=True, sync_tokens=[":", ",", "->"])
        self.match(":", sync_tokens=["Тип данных (Int, String, Float, Bool)", "Int", "String", "Bool", "Float", ",", "->"])
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