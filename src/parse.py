# Parsing Module


import re, sys, io

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
    code = code.replace('\'', ' \' ').replace('\"', ' \" ').replace(';', ' ;').split()
    return code

# Read an expression from a sequence of tokens
# Tokenize and parse strings and comments as quotes
def read_from_tokens(tokens):
    token = tokens.pop(0)
    if '(' == token:
        L = []
        i = 0
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
            i+=1
        tokens.pop(0)
        if i:
            return L
        else:
            return '()'
    elif '"' == token:
        L = []
        while tokens[0] != '"':
            L.append(read_from_tokens(tokens))
        end_quote = tokens.pop(0)
        string = token
        string += " ".join(L)
        string += end_quote
        return ['quote',  string]
    elif '\'' == token:
        return ['quote', tokens.pop(0)]
    else:
        return atom(token)

# Numbers become numbers; every other token is a symbol.
def atom(token):
    try: 
        return int(token)
    except ValueError:
        try: 
            return float(token)
        except ValueError:
            return Symbol(token)

# Read a Lisp expression from a string.
def parse(code):
    return read_from_tokens(tokenize(code))