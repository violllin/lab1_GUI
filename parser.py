from ast_nodes import *

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

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self):
        self.pos += 1

    def match(self, expected, is_type=False, sync_tokens=None):
        token = self.current_token()

        is_match = False
        if token:
            if is_type:
                is_match = (token.type_name == expected)
            else:
                is_match = (token.lexeme == expected)

        if is_match:
            self.advance()
            return True
        else:
            self.errors.append(ParseError(token, expected))
            self.irons_recover(expected, is_type, sync_tokens, error_token=token)
            return False

    def irons_recover(self, expected, is_type, sync_tokens, error_token=None):
        sync_list = sync_tokens or []
        last_extra_lexeme = None

        while self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            is_exp = (is_type and token.type_name == expected) or (not is_type and token.lexeme == expected)
            is_sync = token.lexeme in sync_list or token.type_name in sync_list

            if is_exp or is_sync:
                return

            if token != error_token and token.lexeme != last_extra_lexeme:
                self.errors.append(ParseError(token, expected, f"Лишний символ: '{token.lexeme}'"))
                last_extra_lexeme = token.lexeme

            self.advance()

        raise StopParsing()

    def parse(self):
        ast_root = None
        if not self.tokens:
            return self.errors, ast_root

        try:
            ast_root = self.parse_start()
        except StopParsing:
            pass

        while self.current_token() is not None:
            token = self.current_token()
            self.errors.append(ParseError(token, "конец файла", f"Лишний символ в конце файла: '{token.lexeme}'"))
            self.advance()

        return self.errors, ast_root

    def parse_start(self):
        self.match("let", sync_tokens=["идентификатор", "=", "{"])

        id_tok = self.current_token()
        self.match("идентификатор", is_type=True, sync_tokens=["=", "{"])

        self.match("=", sync_tokens=["{"])
        self.match("{", sync_tokens=["("])
        self.match("(", sync_tokens=["идентификатор", ")", "->"])

        params = []
        if self.current_token() and self.current_token().lexeme != ")":
            params = self.parse_param_list()

        self.match(")", sync_tokens=["->", "in"])
        self.match("->", sync_tokens=["Int", "String", "Float", "Bool", "in"])

        type_tok = self.current_token()
        self.parse_type()

        self.match("in", sync_tokens=["return", "идентификатор", "константа", "("])
        self.match("return", sync_tokens=["идентификатор", "константа", "("])

        body = self.parse_expr()

        self.match("}", sync_tokens=[";"])
        self.match(";")

        return LetNode(id_tok, LambdaNode(params, type_tok, body))

    def parse_param_list(self):
        params = []
        while self.current_token() and self.current_token().lexeme == ",":
            self.errors.append(ParseError(self.current_token(), "идентификатор", "Лишняя запятая"))
            self.advance()

        p = self.parse_param()
        if p: params.append(p)

        while self.current_token() and self.current_token().lexeme not in [")", "->", "in"]:
            if self.current_token().lexeme == ",":
                self.advance()
                while self.current_token() and self.current_token().lexeme == ",":
                    self.errors.append(ParseError(self.current_token(), "идентификатор", "Лишняя запятая"))
                    self.advance()

                if self.current_token() and self.current_token().lexeme == ")":
                    self.errors.append(
                        ParseError(self.current_token(), "идентификатор", "Ожидался параметр после запятой"))
                    break
            else:
                if self.current_token().type_name == "идентификатор":
                    self.errors.append(ParseError(self.current_token(), ",", "Пропущена запятая между параметрами"))
                else:
                    break

            p = self.parse_param()
            if p: params.append(p)
        return params

    def parse_param(self):
        if not self.current_token() or self.current_token().lexeme in [")", "->", "in"]:
            return None

        id_tok = self.current_token()
        if not self.match("идентификатор", is_type=True, sync_tokens=[":", ",", ")", "->"]):
            return None

        type_tok = None
        token = self.current_token()
        if token and token.lexeme == ":":
            self.advance()
            type_tok = self.current_token()
            self.parse_type()
        else:
            self.errors.append(ParseError(token, ":", f"Пропущено ':' после '{id_tok.lexeme}'"))
            if token and token.lexeme in ["Int", "String", "Float", "Bool"]:
                type_tok = self.current_token()
                self.parse_type()

        return ParamNode(id_tok, type_tok)

    def parse_type(self):
        types = ["Int", "String", "Float", "Bool"]
        token = self.current_token()
        last_extra_lexeme = None

        while self.pos < len(self.tokens):
            t = self.tokens[self.pos]
            if t.lexeme in types:
                self.advance()
                return True
            if t.lexeme in [")", "in", "return", "{", "}", ";", ",", "->"]:
                return False

            if t != token and t.lexeme != last_extra_lexeme:
                self.errors.append(ParseError(t, "Тип данных", f"Лишний символ: '{t.lexeme}'"))
                last_extra_lexeme = t.lexeme

            self.pos += 1
        raise StopParsing()

    def parse_expr(self):
        node = self.parse_term()
        while self.current_token() and self.current_token().lexeme in ["+", "-"]:
            op_tok = self.current_token()
            self.advance()
            right = self.parse_term()
            node = BinOpNode(node, op_tok, right)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.current_token() and self.current_token().lexeme in ["*", "/", "%"]:
            op_tok = self.current_token()
            self.advance()
            right = self.parse_factor()
            node = BinOpNode(node, op_tok, right)
        return node

    def parse_factor(self):
        token = self.current_token()
        if not token:
            return None

        if token.type_name == "идентификатор":
            self.advance()
            return VarNode(token)
        elif token.type_name == "константа":
            self.advance()
            return LiteralNode(token)
        elif token.lexeme == "(":
            self.advance()
            node = self.parse_expr()
            self.match(")", sync_tokens=["+", "-", "*", "/", "}", ";"])
            return node
        else:
            self.errors.append(ParseError(token, "Выражение"))
            self.irons_recover("идентификатор", True, ["+", "-", "*", "/", "}", ")", "return"], error_token=token)
            return None