from eval import *

def evaluate_command(inpt):
    val = eval(parse(inpt))
    if val is not None:
        if (lispstr(val) == "True"):
            print("T")
        elif (lispstr(val) == "False"):
            print("()")
        else:
            print((lispstr(val))) # this prints the output of the expression

# A prompt-read-eval-print loop.
def repl(prompt='-> '):
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        open_file = open(file_name, 'r')
        lisp_commands = open_file.readlines()
        for line in lisp_commands:
            inpt = line.strip()
            if inpt == "quit": break
            evaluate_command(inpt)
    else:
        while True:
            inpt = input(prompt)
            if inpt == "quit": break
            evaluate_command(inpt)

# Convert a Python object back into a Lisp-readable string.
def lispstr(exp):
    if isinstance(exp, list):
        return '(' + ' '.join(map(lispstr, exp)) + ')'
    else:
        return str(exp)

print()
repl()
