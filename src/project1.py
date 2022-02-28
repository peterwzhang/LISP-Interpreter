import sys
import operator as op

# class containing symbols (all are python strings)
class Symbol(str): pass
Symbol = str


symbol_dict = {}
# find symbol in symbol_dict or create symbol entry in table
def Sym(s):
    if s not in symbol_dict:
        symbol_dict[s] = Symbol(s)
    return symbol_dict[s]

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
        # the following will be either NULL or an expresion
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
        return ['string', tokens.pop(0)]
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

# the following are the function definitons of required functionality
# Sym() adds the functions to the list of symbols
_string = Sym('string')
_if = Sym('if')
_set = Sym('set')
_print = Sym('print')
_while = Sym('while')

# evaluates expression x within env as defined above
def eval(x):
    if isinstance(x, Symbol):
        # checks if x is a symbol
        return env[x]
    elif not isinstance(x, list):
        # checks if x is not a list
        return x
    elif x[0] == _string:
        # "quoted" or unevaluated expression
        (_, quoted_str) = x
        return quoted_str
    elif x[0] == _if:
        # if statement evaluation 
        (_, test, if_true, if_false) = x
        result = (if_true if eval(test) else if_false)
        return eval(result)
    elif x[0] == _set:
        # sets var to expression
        (_, var, expression) = x
        env[var] = eval(expression)
        return env[var]
    elif x[0] == _print:
        # prints x (and returns so is output twice)
        (_, print_statement) = x
        print(eval(print_statement))
        return eval(print_statement)
    elif x[0] == _while:
        # while loop evaluation
        (_, test, expBody) = x
        while (eval(test)):
            exp = expBody
            eval(exp)
        return ()
    else:
        # if x is not in the above defined finctions (if, set, print, while)
        # evaluate the expression, return solution 
        func = eval(x[0])
        args = [eval(arg) for arg in x[1:]]
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
