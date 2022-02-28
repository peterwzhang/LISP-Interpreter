# Evaluating Module

from parse import *
import math
import operator as op

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

_quote = Sym('quote')
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
    elif x[0] == _quote: # quotation
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

