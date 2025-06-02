import sys
from thorn_interpreter import ThornInterpreter

def run_file(filename):
    print(f"▶ Running: {filename}\n")
    interpreter = ThornInterpreter()
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                interpreter.execute(line)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python runner.py <path-to-file.thorn>")
    else:
        run_file(sys.argv[1])
