class SemanticError:
    def __init__(self, token, message):
        self.token = token
        self.message = message


class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = [{}]
        self.errors = []

    def declare(self, token, type_name):
        if not token: return
        scope = self.symbol_table[-1]
        if token.lexeme in scope:
            self.errors.append(
                SemanticError(token, f"Семантическая ошибка: идентификатор '{token.lexeme}' уже объявлен ранее"))
        else:
            scope[token.lexeme] = type_name

    def lookup(self, token):
        if not token: return "Unknown"
        for scope in reversed(self.symbol_table):
            if token.lexeme in scope:
                return scope[token.lexeme]
        self.errors.append(
            SemanticError(token, f"Семантическая ошибка: неразрешенный идентификатор '{token.lexeme}' (не объявлен)"))
        return "Unknown"

    def analyze(self, ast_root):
        self.errors = []
        self.visit(ast_root)
        return self.errors

    def visit(self, node):
        if not node: return "Unknown"
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        return "Unknown"

    def visit_LetNode(self, node):
        if node.name_tok:
            self.declare(node.name_tok, "Lambda")
        self.visit(node.lambda_node)
        return "Lambda"

    def visit_LambdaNode(self, node):
        self.symbol_table.append({})
        for param in node.params:
            self.visit(param)

        expr_type = self.visit(node.body)

        if node.return_type_tok and expr_type != "Unknown":
            decl_type = node.return_type_tok.lexeme
            if decl_type == "Int" and expr_type not in ["Int"]:
                self.errors.append(SemanticError(node.return_type_tok,
                                                 f"Семантическая ошибка: выражение возвращает '{expr_type}', а ожидается '{decl_type}'"))

        self.symbol_table.pop()
        return "Lambda"

    def visit_ParamNode(self, node):
        if node.name_tok and node.type_tok:
            self.declare(node.name_tok, node.type_tok.lexeme)
        return "Void"

    def visit_BinOpNode(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        return left_type if left_type != "Unknown" else "Int"

    def visit_VarNode(self, node):
        return self.lookup(node.token)

    def visit_LiteralNode(self, node):
        if not node.token: return "Unknown"

        if node.token.type_name == "константа":
            try:
                val = int(node.token.lexeme)
                if val < -2147483648 or val > 2147483647:
                    self.errors.append(SemanticError(node.token,
                                                     f"Семантическая ошибка: значение {val} выходит за пределы 32-битного Int"))
            except ValueError:
                pass
            return "Int"
        elif node.token.lexeme in ["true", "false"]:
            return "Bool"
        return "String"