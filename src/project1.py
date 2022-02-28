import sys
import math
import operator as op

# Class for LISP common symbols
class Symbol(str): pass
Symbol = str
List   = list

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
        token = tokens.pop(0)
        if token == '(':
            token_list = []
            while tokens[0] != ')':
                token_list.append(tokens.pop(0))
            tokens.pop(0)
            return ['string', token_list]
        return ['string', token]
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

def begin(*x):
    return x[-1]

def car(x):
    return x[0]

def cdr(x):
    return x[1:]

def cons(x, y):
    return [x] + [y]

def isList(x):
    return isinstance(x,list)

def isNull(x):
    if x:
        return False
    else:
        return True

def isNum(x):
    return isinstance(x,int) or isinstance(x, float)

def isSymbol(x):
    return isinstance(x, Symbol)

env = {
    '+':op.add,
    '-':op.sub,
    '*':op.mul,
    '/':div,
    '>':op.gt,
    '<':op.lt,
    '=':op.eq,
    'begin': begin,
    'car': car,
    'cdr': cdr,
    'cons': cons,
    'list?':   isList,
    'null?':   isNull,
    'number?': isNum,
    'symbol?': isSymbol,
    'T': 'T',
    '()': False
}

_string = Sym('string')
_if = Sym('if')
_set = Sym('set')
_print = Sym('print')
_while = Sym('while')

# Evaluate an expression in an environment.
def eval(x):
    if isinstance(x, Symbol): # variable reference
        return env[x]
    elif not isinstance(x, list): # constant literal
        return x
    elif x[0] == _string: # quotation
        (_, exp) = x
        return exp
    elif x[0] == _if: # conditional 
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test) else alt)
        return eval(exp)
    elif x[0] == _set: # assignment
        (_, var, exp) = x
        env[var] = eval(exp)
        return env[var]
    elif x[0] == _print: # print
        (_, lst) = x
        print(eval(lst))
        return print(eval(lst))
    elif x[0] == _while: #while loop
        (_, test, conseq) = x
        while (eval(test)):
            exp = conseq
            eval(exp)
        return ()
    else: # 
        proc = eval(x[0])
        args = [eval(arg) for arg in x[1:]]
        return proc(*args)


# Main Module

def evaluate_command(inpt):
    val = eval(parse(inpt))
    if val is not None:
        if (to_str(val) == "True"):
            print("T")
        elif (to_str(val) == "False"):
            print("()")
        else:
            print((to_str(val))) # this prints the output of the expression

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
def to_str(exp):
    if isinstance(exp, list):
        return '(' + ' '.join(map(to_str, exp)) + ')'
    else:
        return str(exp)

print()
repl()
