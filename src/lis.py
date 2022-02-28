import sys
import math
import operator as op

# Class for LISP common symbols
class Symbol(str): pass
Symbol = str
List   = list
Number = (int, float)

symbol_table = {}

# Find or create unique Symbol entry for str s in symbol table
def Sym(s):
    if s not in symbol_table:
        symbol_table[s] = Symbol(s)
    return symbol_table[s]

# Tokenize input string
# Seperate special characters [" ( ) ;) from expression
# Tokens split by spaces
def tokenize(code):
    code = code.replace('(', ' ( ').replace(')', ' ) ')
    code = code.replace('\'', ' \' ') 
    code = code.split()
    return code

# Read an expression from a sequence of tokens
# Tokenize and parse strings and comments as strings
def read_from_tokens(tokens):
    token = tokens.pop(0)
    if '(' == token:
        token_list = []
        i = 0
        while tokens[0] != ')':
            token_list.append(read_from_tokens(tokens))
            i+=1
        tokens.pop(0)
        if i:
            return token_list
        else:
            return '()'
    elif '\'' == token:
        return ['string', tokens.pop(0)]
    else:
        return atom(token)

# Numbers become numbers; every other token is a symbol.
def atom(token):
    if token.isnumeric():
        return int(token)
    elif '.' in token:
        test = token.replace('.', '')
        if test.isnumeric():
            return float(token)
    else:
        return Symbol(token)

# Read a Lisp expression from a string.
def parse(code):
    return read_from_tokens(tokenize(code))



# Evaluating Module

def div(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a // b
    else:
        return a / b


# A user-defined Lisp procedure.
class Procedure(object):
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env

    def __call__(self, *args):
        return eval(self.body, Env(self.parms, args, self.env))


# An environment: a dict with an outer Env.
class Env(dict):
    def __init__(self, parms=(), args=(), outer=None):
        self.update(list(zip(parms, args)))
        self.outer = outer

    # Find the innermost Env where var appears.
    def find(self, var):
        return self if (var in self) else self.outer.find(var)

# An environment with some Lisp standard procedures."
def standard_env():
    env = Env()
    env.update(vars(math))
    env.update({
        '+':op.add,
        '-':op.sub,
        '*':op.mul,
        '/':div,
        '>':op.gt,
        '<':op.lt,
        '=':op.eq,
        'begin': lambda *x: x[-1],
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'cons': lambda x,y: [x] + [y],
        'list?':   lambda x: (isinstance(x,list)),
        'null?':   lambda x: x == [],
        'number?': lambda x: isinstance(x, Number),
        'symbol?': lambda x: isinstance(x, Symbol),
        'T': 'T',
        '()': False
        })
    return env

global_env = standard_env()

_string = Sym('string')
_if = Sym('if')
_set = Sym('set')
_define = Sym('define')
_print = Sym('print')
_while = Sym('while')

# Evaluate an expression in an environment.
def eval(x, env=global_env):
    if isinstance(x, Symbol): # variable reference
        return env.find(x)[x]
    elif not isinstance(x, list): # constant literal
        return x
    elif x[0] == _string: # quotation
        (_, exp) = x
        return exp
    elif x[0] == _if: # conditional
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif x[0] == _define: # definition
        (_, name, parms, body) = x
        env[name] = Procedure(parms, body, env)
        return name
    elif x[0] == _set: # assignment
        (_, var, exp) = x
        env[var] = eval(exp)
        return env[var]
    elif x[0] == _print: # print
        (_, lst) = x
        print(eval(lst, env))
        return print(eval(lst, env))
    elif x[0] == _while: #while loop
        (_, test, conseq) = x
        while (eval(test, env)):
            exp = conseq
            eval(exp, env)
        return () #*dog ear*
    else: # 
        proc = eval(x[0], env)
        args = [eval(arg, env) for arg in x[1:]]
        return proc(*args)


# Main Module

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
