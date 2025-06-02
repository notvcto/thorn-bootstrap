class ThornInterpreter:
    def __init__(self):
        self.env = {}

    def evaluate(self, expr):
        expr = expr.strip()
        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]
        elif '+' in expr:
            parts = expr.split('+')
            return ''.join(self.evaluate(part) for part in parts)
        elif expr in self.env:
            return self.env[expr]
        else:
            raise Exception(f"Unknown expression: {expr}")

    def execute(self, line):
        line = line.strip()
        if line.startswith("let "):
            _, name_expr = line.split("let ", 1)
            name, value = [x.strip() for x in name_expr.split("=", 1)]
            self.env[name] = self.evaluate(value)
        elif line.startswith("print(") and line.endswith(")"):
            inner = line[len("print("):-1]
            result = self.evaluate(inner)
            print(result)
        else:
            raise Exception(f"Unknown statement: {line}")
