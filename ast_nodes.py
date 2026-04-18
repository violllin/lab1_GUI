class AstNode:
    def to_string(self, prefix="", is_tail=True):
        pass

    def to_dict(self):
        pass

class LetNode(AstNode):
    def __init__(self, name_tok, lambda_node):
        self.name_tok = name_tok
        self.lambda_node = lambda_node

    def to_string(self, prefix="", is_tail=True):
        if prefix == "":
            res = "LAMBDA EXPRESSION\n"
            name = self.name_tok.lexeme if self.name_tok else "None"
            res += "└── let: \"" + name + "\"\n"
            if self.lambda_node:
                res += self.lambda_node.to_string("    ", True)
            return res
        else:
            res = prefix + ("└── " if is_tail else "├── ") + "LetNode\n"
            child_prefix = prefix + ("    " if is_tail else "│   ")
            name = self.name_tok.lexeme if self.name_tok else "None"
            res += child_prefix + "└── name: \"" + name + "\"\n"
            if self.lambda_node:
                res += self.lambda_node.to_string(child_prefix, True)
            return res


class LambdaNode(AstNode):
    def __init__(self, params, return_type_tok, body):
        self.params = params
        self.return_type_tok = return_type_tok
        self.body = body

    def to_string(self, prefix="", is_tail=True):
        res = prefix + ("└── " if is_tail else "├── ") + "value: LambdaNode\n"
        child_prefix = prefix + ("    " if is_tail else "│   ")

        ret_type = self.return_type_tok.lexeme if self.return_type_tok else "None"
        res += child_prefix + "├── returnType: \"" + ret_type + "\"\n"

        if self.params:
            res += child_prefix + "├── parameters:\n"
            p_prefix = child_prefix + "│   "
            for i, p in enumerate(self.params):
                is_last = (i == len(self.params) - 1)
                res += p.to_string(p_prefix, is_last)

        if self.body:
            res += child_prefix + "└── body:\n"
            res += self.body.to_string(child_prefix + "    ", True)
        return res


class ParamNode(AstNode):
    def __init__(self, name_tok, type_tok):
        self.name_tok = name_tok
        self.type_tok = type_tok

    def to_string(self, prefix="", is_tail=True):
        name = self.name_tok.lexeme if self.name_tok else "None"
        ptype = self.type_tok.lexeme if self.type_tok else "None"
        res = prefix + ("└── " if is_tail else "├── ") + f"param: \"{name}\"\n"
        res += prefix + ("    " if is_tail else "│   ") + f"└── type: \"{ptype}\"\n"
        return res


class BinOpNode(AstNode):
    def __init__(self, left, op_tok, right):
        self.left = left
        self.op_tok = op_tok
        self.right = right

    def to_string(self, prefix="", is_tail=True):
        op = self.op_tok.lexeme if self.op_tok else "None"
        res = prefix + ("└── " if is_tail else "├── ") + f"operation: \"{op}\"\n"
        child_prefix = prefix + ("    " if is_tail else "│   ")

        if self.left:
            res += self.left.to_string(child_prefix, False)
        if self.right:
            res += self.right.to_string(child_prefix, True)
        return res


class VarNode(AstNode):
    def __init__(self, token):
        self.token = token

    def to_string(self, prefix="", is_tail=True):
        name = self.token.lexeme if self.token else "None"
        return prefix + ("└── " if is_tail else "├── ") + f"id: \"{name}\"\n"


class LiteralNode(AstNode):
    def __init__(self, token):
        self.token = token

    def to_string(self, prefix="", is_tail=True):
        val = self.token.lexeme if self.token else "None"
        return prefix + ("└── " if is_tail else "├── ") + f"literal: {val}\n"