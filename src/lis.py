from eval import *

# _quote = Sym('quote')
# _if = Sym('if')
# _set = Sym('set')
# _define = Sym('define')
# _lambda = Sym('lambda')
# _begin = Sym('begin')
# _definemacro = Sym('define-macro')
# _quasiquote = Sym('quasiquote')
# _unquoto = Sym('unquote')
# _unquotesplicing = Sym('unquote-splicing')
# _checkexpect = Sym('check-expect')
# _checkwithin = Sym('check-within')
# _member = Sym('member?')
# _struct = Sym('struct')

def evaluate_command(inpt):
    try:
        val = eval(parse(inpt))
        if val is not None:
            if (lispstr(val) == "True"):
                print("T")
            elif (lispstr(val) == "False"):
                print("()")
            else:
                print((lispstr(val))) # this prints the output of the expression
    except Exception as e:
            print('%s: %s' % (type(e).__name__, e))

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

repl()
