# runner.py — meta-interpreter to bootstrap Thorn

import sys

# -------------------- I/O Helpers --------------------
def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

# -------------------- Thorn Interpreter --------------------
def run_thorn_interpreter_with_target(interpreter_path, target_path):
    source = read_file(interpreter_path)
    env = {
        'print': print,
        'panic': lambda msg: sys.exit(f"[panic] {msg}"),
        'read': read_file
    }
    
    # -------------------- Parsing --------------------
    functions = {}
    lines = source.splitlines()
    i = 0
    
    def parse_fn():
        nonlocal i
        header = lines[i]
        name = header.split()[1].split('(')[0].strip()
        body = []
        i += 1
        while i < len(lines) and not lines[i].startswith('fn'):
            if lines[i].strip() != '':
                body.append(lines[i].strip())
            i += 1
        functions[name] = body

    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('fn '):
            parse_fn()
        else:
            i += 1

    # -------------------- Evaluator --------------------
    def eval_expr(expr, local_env):
        expr = expr.strip()
        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]
        if '+' in expr:
            parts = [eval_expr(p.strip(), local_env) for p in expr.split('+')]
            return ''.join(parts)
        if expr == '{}':
            return {}
        if expr in local_env:
            return local_env[expr]
        if expr in env:
            return env[expr]
        raise Exception(f"Unknown expression: {expr}")

    def exec_line(line, local_env):
        if line.startswith('let '):
            name_val = line[4:].split('=', 1)
            name = name_val[0].strip()
            value = eval_expr(name_val[1], local_env)
            local_env[name] = value
        elif line.startswith('print(') and line.endswith(')'):
            inner = line[6:-1]
            print(eval_expr(inner, local_env))
        elif line.startswith('run_file(') and line.endswith(')'):
            path = eval_expr(line[9:-1], local_env)
            run_thorn_interpreter_with_target(interpreter_path, path)
        else:
            # Fallback for custom function calls (future)
            pass

    # -------------------- Run Entry Function --------------------
    if 'run_file' not in functions:
        raise Exception("No run_file(path) function found in thorn.thorn")

    file_code = read_file(target_path)
    target_lines = file_code.splitlines()
    
    local_env = dict(env)  # initial scope with builtins
    local_env['lines'] = target_lines
    local_env['path'] = target_path

    for line in target_lines:
        exec_line(line.strip(), local_env)

# -------------------- Entry Point --------------------
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python runner.py <thorn_program_file>")
        sys.exit(1)

    print(f">>\n▶ Running: {sys.argv[1]}\n")
    run_thorn_interpreter_with_target("src/thorn.thorn", sys.argv[1])
