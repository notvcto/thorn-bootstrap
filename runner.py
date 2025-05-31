import sys

# Simulated Thorn environment, not final
env = {}

def print_builtin(msg):
    print(msg)

def input_builtin():
    return input("thorn> ")

def panic(msg):
    print(f"[error] {msg}")
    sys.exit(1)

def extract_var_name(line):
    return line.split("=")[0].replace("let", "").strip()

def extract_var_value(line):
    return line.split("=")[1].strip()

def extract_print_arg(line):
    return line.removeprefix("print(").removesuffix(")").strip()

def evaluate(value):
    if value.startswith('"') and value.endswith('"'):
        return value.strip('"')
    elif value in env:
        return env[value]
    elif "+" in value:
        parts = value.split("+")
        return evaluate(parts[0].strip()) + evaluate(parts[1].strip())
    else:
        return value

def repl():
    while True:
        line = input_builtin()

        if line == "exit":
            break

        if line.startswith("let "):
            name = extract_var_name(line)
            raw_value = extract_var_value(line)
            env[name] = evaluate(raw_value)
        elif line.startswith("print("):
            arg = extract_print_arg(line)
            print_builtin(evaluate(arg))
        else:
            panic("Unknown command: " + line)

if __name__ == "__main__":
    repl()
