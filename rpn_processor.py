class RPNStep:

    def __init__(self, op1, op2, operator, result):
        self.op1 = op1
        self.op2 = op2
        self.operator = operator
        self.result = result


class RPNProcessor:
    def __init__(self):
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2}

    def to_rpn(self, tokens):
        output = []
        stack = []

        valid_tokens = [t for t in tokens if t.type_name in ('Number', 'Operator', 'Bracket')]

        for token in valid_tokens:
            if token.type_name == 'Number':
                output.append(token)
            elif token.value == '(':
                stack.append(token)
            elif token.value == ')':
                while stack and stack[-1].value != '(':
                    output.append(stack.pop())
                if stack: stack.pop()
            elif token.type_name == 'Operator':
                while (stack and stack[-1].value != '(' and
                       self.precedence.get(stack[-1].value, 0) >= self.precedence.get(token.value, 0)):
                    output.append(stack.pop())
                stack.append(token)

        while stack:
            output.append(stack.pop())

        return output

    def calculate(self, rpn_tokens):
        stack = []
        steps = []

        try:
            for token in rpn_tokens:
                if token.type_name == 'Number':
                    stack.append(int(token.value))
                elif token.type_name == 'Operator':
                    if len(stack) < 2: return None, []
                    arg2 = stack.pop()
                    arg1 = stack.pop()
                    res = 0

                    if token.value == '+':
                        res = arg1 + arg2
                    elif token.value == '-':
                        res = arg1 - arg2
                    elif token.value == '*':
                        res = arg1 * arg2
                    elif token.value == '/':
                        if arg2 == 0: return "Error: Div by 0", []
                        res = arg1 // arg2
                    elif token.value == '%':
                        res = arg1 % arg2

                    steps.append(RPNStep(arg1, arg2, token.value, res))
                    stack.append(res)

            final_result = stack[0] if stack else 0
            return final_result, steps
        except Exception:
            return "Error", []