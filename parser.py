class SyntaxError:
    def __init__(self, token, message):
        self.token = token
        self.message = message
        self.line = getattr(token, 'line', 0) if token else 0
        self.column = getattr(token, 'column', 0) if token else 0
        self.lexeme = getattr(token, 'lexeme', "EOF") if token else "EOF"
        self.start = getattr(token, 'start', self.column)
        self.end = getattr(token, 'end', self.column)


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

        if self.errors and self.errors[-1].token == err_token and self.errors[-1].message == message:
            return

        self.errors.append(SyntaxError(err_token, message))

    def require(self, expected_lexeme=None, expected_type=None, error_msg="", sync_tokens=None):
        token = self.current_token()

        if token and ((expected_lexeme and token.lexeme == expected_lexeme) or \
                      (expected_type and token.type_name == expected_type)):
            self.pos += 1
            return token

        self.record_error(error_msg or f"Ожидалось: {expected_lexeme or expected_type}")

        if sync_tokens is None:
            sync_tokens = [";", "}", ")", "in", "return"]
        while self.pos < len(self.tokens):
            t = self.tokens[self.pos]

            if (expected_lexeme and t.lexeme == expected_lexeme) or \
                    (expected_type and t.type_name == expected_type):
                self.pos += 1
                return t

            if t.lexeme in sync_tokens:
                break

            self.pos += 1

        return None

    def parse(self):
        if not self.tokens:
            return []
        self.parse_let_decl()
        return self.errors

    def parse_let_decl(self):
        self.require(expected_lexeme="let", error_msg="Ожидалось ключевое слово 'let'",
                     sync_tokens=["идентификатор", "="])
        self.require(expected_type="идентификатор", error_msg="Ожидалось имя переменной", sync_tokens=["=", "{"])
        self.require(expected_lexeme="=", error_msg="Ожидался знак присваивания '='", sync_tokens=["{", "("])
        self.require(expected_lexeme="{", error_msg="Ожидалась открывающая скобка '{'", sync_tokens=["("])
        self.require(expected_lexeme="(", error_msg="Ожидалась открывающая скобка '('",
                     sync_tokens=["идентификатор", ")"])

        token = self.current_token()
        if token and token.lexeme != ")":
            self.parse_param()
            while self.pos < len(self.tokens) and self.current_token() and self.current_token().lexeme != ")":
                if self.current_token().lexeme == ",":
                    self.pos += 1
                    if self.current_token() and self.current_token().lexeme == ")":
                        self.record_error("Неожиданная запятая перед ')'")
                        break
                    self.parse_param()
                elif self.current_token().type_name == "идентификатор":
                    self.record_error("Ожидалась запятая ',' перед следующим параметром")
                    self.parse_param()
                else:
                    self.record_error("Неожиданный токен в списке параметров")
                    self.pos += 1

        self.require(expected_lexeme=")", error_msg="Ожидалась закрывающая скобка ')'",
                     sync_tokens=["->", "in", "return"])
        self.require(expected_lexeme="->", error_msg="Ожидался оператор '->'",
                     sync_tokens=["Int", "Double", "Float", "Bool", "String", "in", "return"])
        self.parse_type()

        self.require(expected_lexeme="in", error_msg="Ожидалось ключевое слово 'in'",
                     sync_tokens=["return", "идентификатор", "}"])
        self.require(expected_lexeme="return", error_msg="Ожидалось ключевое слово 'return'",
                     sync_tokens=["идентификатор", "число", "числовая константа", "(", "}"])

        if self.current_token() and self.current_token().lexeme not in ["}", ";"]:
            self.parse_expr()
        else:
            self.record_error("Ожидалось возвращаемое выражение")

        self.require(expected_lexeme="}", error_msg="Ожидалась закрывающая скобка '}'", sync_tokens=[";"])
        self.require(expected_lexeme=";", error_msg="Ожидалась точка с запятой ';'", sync_tokens=[])

    def parse_param(self):
        self.require(expected_type="идентификатор", error_msg="Ожидалось имя параметра", sync_tokens=[":", ","])
        self.require(expected_lexeme=":", error_msg="Ожидалось ':' после имени параметра",
                     sync_tokens=["Int", "Double", "Float", "Bool", "String", ","])
        self.parse_type()

    def parse_type(self):
        types = ["Int", "Double", "Float", "Bool", "String"]
        token = self.current_token()
        if token and token.lexeme in types:
            self.pos += 1
        else:
            self.record_error(f"Ожидался тип данных ({', '.join(types)})")
            while self.pos < len(self.tokens):
                t = self.tokens[self.pos]
                if t.lexeme in [",", ")", "in", "->", "{", "}", "return"]:
                    break
                self.pos += 1

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
            self.require(expected_lexeme=")", error_msg="Ожидалась закрывающая скобка ')'",
                         sync_tokens=[";", "}", "+", "-", "*", "/", "in", "return"])
        else:
            self.record_error("Ожидалось выражение (идентификатор, число или скобка)")
            if token.lexeme not in [";", "}", ")", "in", "return", "]", ","]:
                self.pos += 1