import sys
import operator as op

# class containing symbols (all are python strings)
class Symbol(str): pass
Symbol = str

# turns input strings into tokens separated by spaces
def tokenize(lisp_expression):
    lisp_expression = lisp_expression.replace('(', ' ( ').replace(')', ' ) ')
    lisp_expression = lisp_expression.replace('\'', ' \' ') 
    lisp_expression = lisp_expression.split()
    return lisp_expression

# reads sequence of tokens and parses strings
def read_from_tokens(tokens):
    token = tokens.pop(0)
    if '(' == token:
        # the following will be either NULL or an expression
        token_list = []
        i = 0
        # makes token_list from all tokens within parentheses
        while tokens[0] != ')':
            token_list.append(read_from_tokens(tokens))
            i+=1
        tokens.pop(0)
        # if i is zero, it's NULL
        if i:
            return token_list
        else:
            return '()'
    elif '\'' == token:
        # the token is a "quoted string" and not evaluated
        token = tokens.pop(0)
        if token == '(':
            token_list = []
            while tokens[0] != ')':
                token_list.append(tokens.pop(0))
            tokens.pop(0)
            return ['string', token_list]
        return ['string', token]
    else:
        # the token is an atom (int, float, or symbol)
        return atom(token)

# returns what kind of atom the token is (int, float, or symbol)
def atom(token):
    if token.isnumeric():
        # if the atom is an int, return int
        return int(token)
    elif '.' in token:
        # if the atom is a float, return float
        test = token.replace('.', '')
        if test.isnumeric():
            return float(token)
    else:
        # if the atom is not an int or float, return symbol
        return Symbol(token)

# parse Lisp expression from string
def parse(lisp_expression):
    # returns the tokenized Lisp command(s)
    return read_from_tokens(tokenize(lisp_expression))

# allow div to compute floordiv or truediv based on types of numbers
def div(a, b):
    if isinstance(a, int) and isinstance(b, int):
        # if both a and b are ints, return floordiv
        return a // b
    else:
        # if a and/or b are floats, return truediv
        return a / b

# returns most recent of any number of args x
def begin(*x):
    return x[-1]

# return the first element of list x
def car(x):
    return x[0]

# return all elements of list x except the first element
def cdr(x):
    return x[1:]

# creates list from x and y
def cons(x, y):
    return [x] + [y]

# if x is a list return T, otherwise return ()
def isList(x):
    return isinstance(x,list)

# if x is NULL return true, otherwise return false
def isNull(x):
    if x:
        return False
    else:
        return True

# if x is an int or a float return T, otherwise return ()
def isNum(x):
    return isinstance(x,int) or isinstance(x, float)

# if x is a symbol return T, otherwise return ()
def isSymbol(x):
    return isinstance(x, Symbol)

# defines environment (dict) of operation definitions
# the key is the operation as it appears in a Lisp command
# the value is the operation as it is executed
env = {
    # 'key': value,
    'begin': begin,
    # the following use python builtin operator library as their definition
    '+':op.add,
    '-':op.sub,
    '*':op.mul,
    # div is defined as a function to allow truediv and floordiv to happen as needed
    '/':div,
    '=':op.eq,
    '<':op.lt,
    '>':op.gt,
    # the following are defined as functions that return the expected value
    'cons': cons,
    'car': car,
    'cdr': cdr,
    'number?': isNum,
    'symbol?': isSymbol,
    'list?':   isList,
    'null?':   isNull,
    # the following are definitions of T and () to mean true and false
    'T': 'T',
    '()': False
}

envList = [env]


class Procedure(object):
    def __init__(self, params, body, outerEnv):
        self.params, self.body, self.outerEnv  = params, body, outerEnv

    def __call__(self, *args):
        envList.append(dict(zip(self.params, args))) 
        self.index = len(envList) - 1
        return eval(self.body[0], dict(zip(self.params, args)), self.index)
        
def getEnvInd(x):
    i = len(envList) - 1
    while x not in envList[i]:
        if i == 0:
            break
        i -= 1
    return i

# evaluates expression x within env as defined above
def eval(x, env=envList[0], envI=0):
    if isinstance(x, Symbol):
        # checks if x is a symbol
        if x in env: return env[x]
        else: return envList[getEnvInd(x)][x]
    elif not isinstance(x, list):
        # checks if x is not a list
        return x
    elif x[0] == 'string':
        # "quoted" or unevaluated expression
        (_, quoted_str) = x
        return quoted_str
    elif x[0] == 'define':
        (params, *body) = x[2:]
        env[x[1]] = Procedure(params, body, env)
        return x[1]
    elif x[0] == 'if':
        # if statement evaluation 
        (_, test, if_true, if_false) = x
        result = (if_true if eval(test, env, envI) else if_false)
        return eval(result, env, envI)
    elif x[0] == 'set':
        # sets var to expression
        (_, var, expression) = x
        env[var] = eval(expression, env, envI)
        return env[var]
    elif x[0] == 'print':
        # prints x (and returns so is output twice)
        (_, print_statement) = x
        print(eval(print_statement, env, envI))
        return eval(print_statement, env, envI)
    elif x[0] == 'while':
        # while loop evaluation
        (_, test, expBody) = x
        while (eval(test, env, envI)):
            exp = expBody
            eval(exp, env, envI)
        return ()
    else:
        # if x is not in the above defined finctions (if, set, print, while, define)
        # evaluate the expression, return solution 
        func = eval(x[0], env, envI)
        args = [eval(arg, env, getEnvInd(func)) for arg in x[1:]]
        return func(*args)

# evaluates the command provided either in a test file or in line-by-line input
def evaluate_command(lisp_input):
    # evaluates input
    val = eval(parse(lisp_input))
    if val is not None:
        if (to_str(val) == "True"):
            # if value is true print T
            print("T")
        elif (to_str(val) == "False"):
            # if value is false print ()
            print("()")
        else:
            # prints output of expression (if not T or ())
            print((to_str(val)))

# gets input of Lisp commands
def get_input():
    if len(sys.argv) > 1:
        # if a test file is provided as argument, use lines of test file as input
        # outputs results of each line to stdout
        file_name = sys.argv[1]
        open_file = open(file_name, 'r')
        lisp_commands = open_file.readlines()
        for line in lisp_commands:
            lisp_input = line.strip()
            if lisp_input == "quit":
                break
            evaluate_command(lisp_input)
    else:
        # if a test file is not provided as argument, use line by line user input as input
        # outputs results of each expression to stdout
        while True:
            lisp_input = input('-> ')
            if lisp_input == "quit":
                break
            evaluate_command(lisp_input)

# puts expression back in Lisp form
def to_str(exp):
    if isinstance(exp, list):
        # if the expression is a list, convert all elements of list back to Lisp form
        return '(' + ' '.join(map(to_str, exp)) + ')'
    else:
        # if the expression is not a list, the Lisp espression is equivalent, return the expression
        return str(exp)

print()
get_input()
