import sys

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def run_thorn_interpreter_with_target(interpreter_path, target_path):
    env = {
        "print": print,
        "panic": lambda msg: sys.exit(f"[panic] {msg}"),
        "read": read_file
    }

    # Load interpreter source
    lines = read_file(interpreter_path).splitlines()

    # Append call to run_file("program_path")
    lines.append(f'run_file("{target_path}")')

    def eval_expr(expr):
        expr = expr.strip()

        # String literal
        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]

        # Concatenation with +
        if "+" in expr:
            parts = [eval_expr(p.strip()) for p in expr.split("+")]
            return "".join(parts)

        # Empty dict literal
        if expr == "{}":
            return {}

        # Function call
        if expr.endswith(")") and "(" in expr:
            fname, argstr = expr.split("(", 1)
            fname = fname.strip()
            args = [eval_expr(a.strip()) for a in argstr[:-1].split(",") if a.strip()]
            if fname in env and callable(env[fname]):
                return env[fname](*args)

        # Variable lookup
        if expr in env:
            return env[expr]

        raise Exception(f"Unknown expression: {expr}")

    def parse_block(start_idx, lines):
        block = []
        depth = 0
        i = start_idx
        while i < len(lines):
            line = lines[i].strip()
            if "{" in line:
                depth += line.count("{")
            if "}" in line:
                depth -= line.count("}")
            block.append(line)
            if depth == 0:
                break
            i += 1
        return block, i

    def exec_line(line):
        line = line.strip()
        if not line or line.startswith("#"):
            return

        if line.startswith("let "):
            name_val = line[4:].split("=", 1)
            name = name_val[0].strip()
            value = eval_expr(name_val[1])
            env[name] = value
            return

        if line.startswith("print(") and line.endswith(")"):
            inner = line[6:-1]
            print(eval_expr(inner))
            return

        if line.startswith("run_file(") and line.endswith(")"):
            path = line[9:-1].strip('"')
            nested_lines = read_file(path).splitlines()
            for nested in nested_lines:
                exec_line(nested)
            return

        raise Exception(f"Unknown line: {line}")

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("fn "):
            # e.g. fn name(arg) {
            header = line[3:].split("(", 1)
            fname = header[0].strip()
            args = header[1].split(")", 1)[0].strip().split(",")
            args = [a.strip() for a in args if a.strip()]
            block, new_i = parse_block(i, lines)
            body = block[1:-1]  # remove opening and closing braces
            def make_fn(args, body):
                def _fn(*passed_args):
                    local_env = env.copy()
                    for k, v in zip(args, passed_args):
                        local_env[k] = v
                    for bl in body:
                        exec_line_in_env(bl, local_env)
                return _fn
            env[fname] = make_fn(args, body)
            i = new_i + 1
            continue

        exec_line(line)
        i += 1

    def exec_line_in_env(line, local_env):
        line = line.strip()
        if not line or line.startswith("#"):
            return

        if line.startswith("let "):
            name_val = line[4:].split("=", 1)
            name = name_val[0].strip()
            value = eval_expr_with_env(name_val[1], local_env)
            local_env[name] = value
            return

        if line.startswith("print(") and line.endswith(")"):
            inner = line[6:-1]
            print(eval_expr_with_env(inner, local_env))
            return

        if line.startswith("run_file(") and line.endswith(")"):
            path = line[9:-1].strip('"')
            nested_lines = read_file(path).splitlines()
            for nested in nested_lines:
                exec_line_in_env(nested, local_env)
            return

        raise Exception(f"Unknown line in fn: {line}")

    def eval_expr_with_env(expr, local_env):
        expr = expr.strip()

        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]

        if "+" in expr:
            parts = [eval_expr_with_env(p.strip(), local_env) for p in expr.split("+")]
            return "".join(parts)

        if expr == "{}":
            return {}

        if expr.endswith(")") and "(" in expr:
            fname, argstr = expr.split("(", 1)
            fname = fname.strip()
            args = [eval_expr_with_env(a.strip(), local_env) for a in argstr[:-1].split(",") if a.strip()]
            if fname in local_env and callable(local_env[fname]):
                return local_env[fname](*args)

        if expr in local_env:
            return local_env[expr]

        raise Exception(f"Unknown expression in fn: {expr}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python runner.py <thorn_program_file>")
        sys.exit(1)

    print(f">>\n▶ Running: {sys.argv[1]}\n")
    run_thorn_interpreter_with_target("src/thorn.thorn", sys.argv[1])
