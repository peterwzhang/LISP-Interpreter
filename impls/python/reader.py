import re


class Reader:
    def __init__(self, t, p=0):
        self.tokens = t
        self.position = p

    def next(self):
        returnToken = self.tokens[self.position]
        position += 1
        return returnToken

    def peek(self):
        return self.tokens[self.position]

def tokenize(str):
    pattern = re.compile(r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"?|;.*|[^\s\[\]{}('"`,;)]*)""")
    return re.findall(pattern, str)

def read_form(reader):
    curTkn = reader.peak()
    if curTkn == ';':
        reader.next()
        return None
    elif curTkn == '\'':
        reader.next()
        # return _list(_symbol('quote'), read_form(reader))
    elif curTkn == '`':
        reader.next()
        # return _list(_symbol('quasiquote'), read_form(reader))
    elif curTkn == '~':
        reader.next()
        # return _list(_symbol('unquote'), read_form(reader))
    elif curTkn == '~@':
        reader.next()
        # return _list(_symbol('splice-unquote'), read_form(reader))
    elif curTkn == '^':
        reader.next()
        meta = read_form(reader)
        # return _list(_symbol('with-meta'), read_form(reader), meta)
    elif curTkn == '@':
        reader.next()
        # return _list(_symbol('deref'), read_form(reader))

def read_str(str):
    tokens = tokenize(str)
    reader = Reader(tokens)
    return read_form(reader)