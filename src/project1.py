import sys
import operator as op

# class containing symbols (all are python strings)
# symbols are defined as non-numbers (not ints or floats)
class Symbol(str): pass
Symbol = str

#=============================================================================
#
# Function definitions of all built-in functionality for the interpreter that
# are not built into python including begin, div (combination of truediv and
# floordiv), cons, car, cdr, number?, symbol?, list?, null?
#
#=============================================================================

# returns most recent of any number of args x
def begin(*x):
    return x[-1]

# allow div to compute floordiv or truediv based on types of numbers
def div(a, b):
    if isinstance(a, int) and isinstance(b, int):
        # if both a and b are ints, return floordiv
        return a // b
    else:
        # if a and/or b are floats, return truediv
        return a / b

# creates list from x and y
def cons(x, y):
    return [x] + [y]

# return the first element of list x
def car(x):
    return x[0]

# return all elements of list x except the first element
def cdr(x):
    return x[1:]

# if x is an int or a float return T, otherwise return ()
def isNum(x):
    return isinstance(x,int) or isinstance(x, float)

# if x is a symbol return T, otherwise return ()
def isSymbol(x):
    return isinstance(x, Symbol)

# if x is a list return T, otherwise return ()
def isList(x):
    return isinstance(x,list)

# if x is NULL return true, otherwise return false
def isNull(x):
    if x:
        return False
    else:
        return True

#=============================================================================
#
# defines environment (dict) of operation definitions
# the key is the operation as it appears in a Lisp command
# the value is the operation as it is executed
#
#=============================================================================

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

#=============================================================================
#
# Evaluation of Lisp commands by using the environment as defined above and/or
# user defined functions appended to the environment list
#
#=============================================================================

# list containing global environment (all required functionality as defined in project description)
# user defined functions are appended to this list
envList = [env]

# returns the index of the function (where it's found in the environment list)
def getEnvInd(x):
    i = len(envList) - 1
    # goes through every element in the environment list
    while x not in envList[i]:
        # when the function is found in the list of environments, returns the index of that environment dictionary
        if i == 0:
            break
        i -= 1
    return i

# Procedure is called to define a function
class Procedure(object):
    def __init__(self, params, body, outerEnv):
        # initializes the procedure with the provided parameters, function body, and outer environment
        self.params, self.body, self.outerEnv  = params, body, outerEnv

    def __call__(self, *args):
        # when a predefined function is called:
        # append the new parameters and arguments to the environment list as a dictionary
        envList.append(dict(zip(self.params, args)))
        # set index where function definition can be found within environment list
        self.index = len(envList) - 1
        # evaluates the function with provided arguments
        return eval(self.body[0], dict(zip(self.params, args)), self.index)

# evaluates expression x within env as defined above
def eval(x, env=envList[0], envI=0):
    if isinstance(x, Symbol):
        # checks if x is a symbol
        if x in env: return env[x]
        #finds and returns environment Symbol is in
        else: return envList[getEnvInd(x)][x]
    elif not isinstance(x, list):
        # checks if x is not a list
        return x
    elif x[0] == 'string':
        # "quoted" or unevaluated expression
        (_, quoted_str) = x
        return quoted_str
    elif x[0] == 'define':
        # defines a function with params and function body as defined by user
        (params, *body) = x[2:]
        # creates the procedure for the user defined function
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
        # evaluate the function, return solution
        # calls function
        func = eval(x[0], env, envI)
        # sets arguments to values as defined in function call
        args = [eval(arg, env, getEnvInd(func)) for arg in x[1:]]
        # returns evaluated function
        return func(*args)

#=============================================================================
#
# Reads from tokenized (see below) strings, parses the tokens so they can be
# interpreted by the program
#
#=============================================================================

# returns what kind of atom the token is (int, float, or symbol)
def atomType(token):
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

# reads sequence of tokens and parses strings
def readTokens(tokens):
    token = tokens.pop(0)
    if '(' == token:
        # the following will be either NULL or an expression
        token_list = []
        i = 0
        # makes token_list from all tokens within parentheses
        while tokens[0] != ')':
            token_list.append(readTokens(tokens))
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
        return atomType(token)

#=============================================================================
#
# Turns input into tokens, parses tokens as parts of Lisp expressions
# Ensures output is in correct lisp formatting (toStr())
#
#=============================================================================

# turns input strings into tokens separated by spaces
def toTokens(lisp_expression):
    lisp_expression = lisp_expression.replace('(', ' ( ').replace(')', ' ) ')
    lisp_expression = lisp_expression.replace('\'', ' \' ')
    lisp_expression = lisp_expression.split()
    return lisp_expression

# parse Lisp expression from string
def parse(lisp_expression):
    # returns the tokenized Lisp command(s)
    return readTokens(toTokens(lisp_expression))

# puts expression back in Lisp form
def toStr(exp):
    if isinstance(exp, list):
        # if the expression is a list, convert all elements of list back to Lisp form
        return '(' + ' '.join(map(toStr, exp)) + ')'
    else:
        # if the expression is not a list, the Lisp espression is equivalent, return the expression
        return str(exp)

#=============================================================================
#
# Gets Lisp commands from repl or from an input test file
# Evaluates commands by calling eval() as defined above
#
#=============================================================================

# evaluates the command provided either in a test file or by repl
def evaluateCommand(lisp_input):
    # evaluates input
    val = eval(parse(lisp_input))
    if val is not None:
        if (toStr(val) == "True"):
            # if value is true print T
            print("T")
        elif (toStr(val) == "False"):
            # if value is false print ()
            print("()")
        else:
            # prints output of expression (if not T or ())
            print((toStr(val)))

# gets input of Lisp commands either by repl or from input file
def getInput():
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
            evaluateCommand(lisp_input)
    else:
        # if a test file is not provided as argument, use repl
        # outputs results of each expression to stdout
        while True:
            lisp_input = input('-> ')
            if lisp_input == "quit":
                break
            evaluateCommand(lisp_input)

# extra print statement included so test results match Kamin C++ results
print()
# calls getInput(), begins reading input
getInput()
