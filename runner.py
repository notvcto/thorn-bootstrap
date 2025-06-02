import sys

def read_file(path):
    with open(path, 'r') as f:
        return f.read()

def run_thorn_file(path):
    content = read_file(path)
    lines = content.splitlines()

    for line in lines:
        if line.strip().startswith("#") or line.strip() == "":
            continue  # Skip comments and blanks
        if line.strip().startswith("run_file("):
            inner = line.strip()[9:-1].strip('"')
            run_thorn_program(inner)

def run_thorn_program(path):
    content = read_file(path)
    lines = content.splitlines()
    env = {}

    def eval_expr(expr):
        expr = expr.strip()

        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]

        if '+' in expr:
            parts = expr.split('+')
            return ''.join(eval_expr(p) for p in parts)

        if expr in env:
            return env[expr]

        raise Exception(f"Unknown expression: {expr}")

    for line in lines:
        line = line.strip()
        if line.startswith("let "):
            _, rest = line.split("let ", 1)
            name, value = [x.strip() for x in rest.split("=", 1)]
            env[name] = eval_expr(value)
        elif line.startswith("print(") and line.endswith(")"):
            inner = line[6:-1]
            print(eval_expr(inner))
        else:
            raise Exception(f"Unknown statement: {line}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python runner.py <interpreter_file>")
        sys.exit(1)

    print(f">>\n▶ Running: {sys.argv[1]}\n")
    run_thorn_file(sys.argv[1])
