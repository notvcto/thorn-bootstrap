import sys

def read_file(path):
    with open(path, 'r') as f:
        return f.read()

def run_thorn_interpreter(interpreter_path, target_path):
    env = {}

    def eval_expr(expr):
        expr = expr.strip()
        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]
        elif '+' in expr:
            parts = expr.split('+')
            return ''.join(eval_expr(part) for part in parts)
        elif expr in env:
            return env[expr]
        else:
            raise Exception(f"Unknown expression: {expr}")

    def exec_line(line):
        line = line.strip()
        if line.startswith("let "):
            rest = line[4:]
            name, value = [x.strip() for x in rest.split("=", 1)]
            env[name] = eval_expr(value)
        elif line.startswith("print(") and line.endswith(")"):
            inner = line[6:-1]
            result = eval_expr(inner)
            print(result)
        else:
            raise Exception(f"Unknown statement: {line}")

    code = read_file(target_path).split("\n")
    for line in code:
        if line.strip():
            exec_line(line)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python runner.py <program_file>")
    else:
        print(f"▶ Running: {sys.argv[1]}\n")
        run_thorn_interpreter("src/thorn.thorn", sys.argv[1])
