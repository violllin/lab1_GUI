class AstNode:
    def to_string(self, prefix="", is_tail=True):
        pass

    def to_dict(self):
        pass


class LetNode(AstNode):
    def __init__(self, name_tok, lambda_node):
        self.name_tok = name_tok
        self.lambda_node = lambda_node

    def to_dict(self):
        return {
            "node": "LetDeclNode",
            "name": self.name_tok.lexeme if self.name_tok else None,
            "lambda": self.lambda_node.to_dict() if self.lambda_node else None
        }

    def to_string(self, prefix="", is_tail=True):
        name = self.name_tok.lexeme if self.name_tok else "None"
        res = prefix + ("└── " if is_tail else "├── ") + f"LetDeclNode (name: {name})\n"
        if self.lambda_node:
            res += self.lambda_node.to_string(prefix + ("    " if is_tail else "│   "), True)
        return res


class LambdaNode(AstNode):
    def __init__(self, params, return_type_tok, body):
        self.params = params
        self.return_type_tok = return_type_tok
        self.body = body

    def to_dict(self):
        return {
            "node": "LambdaNode",
            "return_type": self.return_type_tok.lexeme if self.return_type_tok else None,
            "params": [p.to_dict() for p in self.params],
            "body": self.body.to_dict() if self.body else None
        }

    def to_string(self, prefix="", is_tail=True):
        ret_type = self.return_type_tok.lexeme if self.return_type_tok else "None"
        res = prefix + ("└── " if is_tail else "├── ") + f"LambdaNode (return_type: {ret_type})\n"
        child_prefix = prefix + ("    " if is_tail else "│   ")

        for i, param in enumerate(self.params):
            is_last_param = (i == len(self.params) - 1)
            res += param.to_string(child_prefix, is_tail=(is_last_param and not self.body))

        if self.body:
            res += self.body.to_string(child_prefix, is_tail=True)
        return res


class ParamNode(AstNode):
    def __init__(self, name_tok, type_tok):
        self.name_tok = name_tok
        self.type_tok = type_tok

    def to_dict(self):
        return {
            "node": "ParamNode",
            "name": self.name_tok.lexeme if self.name_tok else None,
            "type": self.type_tok.lexeme if self.type_tok else None
        }

    def to_string(self, prefix="", is_tail=True):
        name = self.name_tok.lexeme if self.name_tok else "None"
        t_name = self.type_tok.lexeme if self.type_tok else "None"
        return prefix + ("└── " if is_tail else "├── ") + f"ParamNode (name: {name}, type: {t_name})\n"


class BinOpNode(AstNode):
    def __init__(self, left, op_tok, right):
        self.left = left
        self.op_tok = op_tok
        self.right = right

    def to_dict(self):
        return {
            "node": "BinOpNode",
            "op": self.op_tok.lexeme if self.op_tok else None,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None
        }

    def to_string(self, prefix="", is_tail=True):
        op = self.op_tok.lexeme if self.op_tok else "None"
        res = prefix + ("└── " if is_tail else "├── ") + f"BinOpNode (op: '{op}')\n"
        child_prefix = prefix + ("    " if is_tail else "│   ")
        if self.left:
            res += self.left.to_string(child_prefix, is_tail=False)
        if self.right:
            res += self.right.to_string(child_prefix, is_tail=True)
        return res


class VarNode(AstNode):
    def __init__(self, token):
        self.token = token

    def to_dict(self):
        return {
            "node": "VarNode",
            "name": self.token.lexeme if self.token else None
        }

    def to_string(self, prefix="", is_tail=True):
        name = self.token.lexeme if self.token else "None"
        return prefix + ("└── " if is_tail else "├── ") + f"VarNode (name: {name})\n"


class LiteralNode(AstNode):
    def __init__(self, token):
        self.token = token

    def to_dict(self):
        return {
            "node": "LiteralNode",
            "value": self.token.lexeme if self.token else None
        }

    def to_string(self, prefix="", is_tail=True):
        val = self.token.lexeme if self.token else "None"
        return prefix + ("└── " if is_tail else "├── ") + f"LiteralNode (value: {val})\n"