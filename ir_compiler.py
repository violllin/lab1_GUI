class TACGenerator:
    def __init__(self):
        self.instructions = []
        self.tmp_count = 0

    def new_temp(self):
        self.tmp_count += 1
        return f"t{self.tmp_count}"

    def generate(self, node):
        self.instructions = []
        self.tmp_count = 0
        self.visit(node)
        return self.instructions

    def visit(self, node):
        if node is None:
            return ""

        node_type = type(node).__name__

        if node_type == "LetNode":
            self.instructions.append(f"define {node.name_tok.lexeme}:")
            self.visit(node.lambda_node)

        elif node_type == "LambdaNode":
            for p in node.params:
                self.instructions.append(f"param {p.name_tok.lexeme}")
            res = self.visit(node.body)
            self.instructions.append(f"return {res}")

        elif node_type == "BinOpNode":
            left = self.visit(node.left)
            right = self.visit(node.right)
            t = self.new_temp()
            self.instructions.append(f"{t} = {left} {node.op_tok.lexeme} {right}")
            return t

        elif node_type == "VarNode":
            return node.token.lexeme

        elif node_type == "LiteralNode":
            return node.token.lexeme


class TACOptimizer:
    @staticmethod
    def fold_constants(instructions):
        optimized = []
        constants = {}
        count = 0

        for inst in instructions:
            parts = inst.split()
            if len(parts) == 5 and parts[1] == '=':
                target, _, left, op, right = parts
                l_val = constants.get(left, left)
                r_val = constants.get(right, right)

                if l_val.lstrip('-').isdigit() and r_val.lstrip('-').isdigit():
                    try:
                        res = str(int(eval(f"{l_val} {op} {r_val}")))
                        constants[target] = res
                        optimized.append(f"{target} = {res}")
                        count += 1
                        continue
                    except:
                        pass

                new_val = None
                if op == '*':
                    if l_val == '0' or r_val == '0':
                        new_val = '0'
                    elif l_val == '1':
                        new_val = r_val
                    elif r_val == '1':
                        new_val = l_val
                elif op == '+':
                    if l_val == '0':
                        new_val = r_val
                    elif r_val == '0':
                        new_val = l_val

                if new_val is not None:
                    constants[target] = new_val
                    optimized.append(f"{target} = {new_val}")
                    count += 1
                else:
                    optimized.append(f"{target} = {l_val} {op} {r_val}")

            elif len(parts) == 3 and parts[1] == '=':
                target, _, val = parts
                actual_val = constants.get(val, val)
                constants[target] = actual_val
                optimized.append(f"{target} = {actual_val}")
            elif inst.startswith("return"):
                val = parts[1]
                optimized.append(f"return {constants.get(val, val)}")
            else:
                optimized.append(inst)

        return optimized, count

    @staticmethod
    def eliminate_dead_code(instructions):
        used_vars = set()
        for inst in instructions:
            parts = inst.split()
            if inst.startswith("return"):
                used_vars.add(parts[1])
            elif len(parts) == 5:
                used_vars.add(parts[2])
                used_vars.add(parts[4])
            elif len(parts) == 3 and parts[1] == '=':
                used_vars.add(parts[2])

        optimized = []
        removed_count = 0
        for inst in instructions:
            parts = inst.split()
            if len(parts) >= 3 and parts[1] == '=' and parts[0].startswith('t'):
                if parts[0] not in used_vars:
                    removed_count += 1
                    continue
            optimized.append(inst)
        return optimized, removed_count

    @staticmethod
    def get_final_result(instructions):
        if not instructions: return "Не определено"
        last_inst = instructions[-1]
        if "return" in last_inst:
            return last_inst.replace("return", "").strip()
        if "=" in last_inst:
            return last_inst.split("=")[-1].strip()
        return "..."