class SyntaxError:
    def __init__(self, token, message):
        self.token = token
        self.message = message
        self.line = getattr(token, 'line', 0)
        self.column = getattr(token, 'column', 0)
        self.lexeme = getattr(token, 'lexeme', "")

class Parser:
    def __init__(self, tokens):
        self.tokens = [t for t in tokens if not getattr(t, 'is_error', False) and t.lexeme != "space"]
        self.pos = 0
        self.errors = []

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def record_error(self, message):
        token = self.current_token()
        err_token = token if token else (self.tokens[-1] if self.tokens else None)
        self.errors.append(SyntaxError(err_token, message))

    def require(self, expected_lexeme=None, expected_type=None, error_msg=""):
        token = self.current_token()

        if token:
            if (expected_lexeme and token.lexeme == expected_lexeme) or \
                    (expected_type and token.type_name == expected_type):
                self.pos += 1
                return token

        self.record_error(error_msg or f"Ожидалось: {expected_lexeme or expected_type}")

        if not token:
            return None

        if self.pos + 1 < len(self.tokens):
            next_t = self.tokens[self.pos + 1]
            if (expected_lexeme and next_t.lexeme == expected_lexeme) or \
                    (expected_type and next_t.type_name == expected_type):
                self.pos += 2
                return next_t

        return None

    def parse(self):
        if not self.tokens:
            return []
        self.parse_let_decl()
        return self.errors

    def parse_let_decl(self):
        self.require(expected_lexeme="let", error_msg="Ожидалось ключевое слово 'let'")
        self.require(expected_type="идентификатор", error_msg="Ожидалось имя переменной (идентификатор)")
        self.require(expected_lexeme="=", error_msg="Ожидался знак присваивания '='")
        self.require(expected_lexeme="{", error_msg="Ожидалась открывающая скобка '{'")
        self.require(expected_lexeme="(", error_msg="Ожидалась открывающая скобка '('")

        token = self.current_token()
        if token and token.lexeme != ")":
            self.parse_param()
            while self.current_token() and self.current_token().lexeme == ",":
                self.pos += 1
                self.parse_param()

        self.require(expected_lexeme=")", error_msg="Ожидалась закрывающая скобка ')'")
        self.require(expected_lexeme="->", error_msg="Ожидался оператор '->'")
        self.parse_type()

        self.require(expected_lexeme="in", error_msg="Ожидалось ключевое слово 'in'")
        self.require(expected_lexeme="return", error_msg="Ожидалось ключевое слово 'return'")

        self.parse_expr()

        self.require(expected_lexeme="}", error_msg="Ожидалась закрывающая скобка '}'")
        self.require(expected_lexeme=";", error_msg="Ожидалась точка с запятой ';'")

    def parse_param(self):
        self.require(expected_type="идентификатор", error_msg="Ожидалось имя параметра")
        self.require(expected_lexeme=":", error_msg="Ожидалось ':' после имени параметра")
        self.parse_type()

    def parse_type(self):
        types = ["Int", "Double", "Float", "Bool", "String"]
        token = self.current_token()
        if token and token.lexeme in types:
            self.pos += 1
        else:
            self.record_error(f"Ожидался тип данных ({', '.join(types)})")
            if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].lexeme in types:
                self.pos += 2

    def parse_expr(self):
        self.parse_term()
        while self.current_token() and self.current_token().lexeme in ["+", "-"]:
            self.pos += 1
            self.parse_term()

    def parse_term(self):
        self.parse_factor()
        while self.current_token() and self.current_token().lexeme in ["*", "/"]:
            self.pos += 1
            self.parse_factor()

    def parse_factor(self):
        token = self.current_token()
        if not token:
            self.record_error("Неожиданный конец: ожидалось выражение")
            return

        if token.type_name in ["идентификатор", "константа", "число", "числовая константа"]:
            self.pos += 1
        elif token.lexeme == "(":
            self.pos += 1
            self.parse_expr()
            self.require(expected_lexeme=")", error_msg="Ожидалась закрывающая скобка ')'")
        else:
            self.record_error("Ожидалось выражение (идентификатор, число или скобка)")
            self.pos += 1