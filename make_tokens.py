from tokenize import tokenize
from io import BytesIO


def read_file(file_name):
    s = ""
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            s += line
    return s


def tokenize_file(str_file):
    tokens = []
    g = tokenize(BytesIO(str_file.encode('utf-8')).readline)
    for toknum, tokval, start, end, line in g:
        tokens.append((toknum, tokval, start, end, line))
    return tokens


def get_encoding(file_name):
    encoding = [
        'utf-8',
        'cp500',
        'utf-16',
        'GBK',
        'windows-1251',
        'ASCII',
        'US-ASCII',
        'Big5'
    ]

    correct_encoding = ''

    for enc in encoding:
        try:
            open(file_name, encoding=enc).read()
        except (UnicodeDecodeError, LookupError):
            pass
        else:
            correct_encoding = enc
            break

    return correct_encoding


def is_function(tokens, i):
    j = 2
    if tokens[i].token_type == "NAME" and tokens[i + 1].content == "(":
        while True:
            try:
                if tokens[i + j].content == ')':
                    return True
                else:
                    j += 1
            except IndexError:
                return False
    return False


def is_func_decl(tokens, i):
    try:
        if tokens[i - 1].content == "def" and tokens[i].token_type == "NAME":
            return True
    except IndexError:
        return False
    return False


def is_class_decl(tokens, i):
    try:
        if tokens[i - 1].content == "class" and tokens[i].token_type == "NAME":
            return True
    except IndexError:
        return False
    return False


def get_class_start(tokens, i):
    try:
        if tokens[i - 1].content == "class" and tokens[i].token_type == "NAME":
            return tokens[i - 1].start
    except IndexError:
        return (-1, -1)
    return (-1, -1)


def is_end(tokens, i, start):
    if tokens[i].start[1] == start[1] and tokens[i].token_type != "INDENT" and tokens[i].content != '\n':
        return True
    return False
