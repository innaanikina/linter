from message import make_message_line, make_full_message, make_mes
from make_tokens import get_encoding, is_function
import configparser
import re


def check_correct_module(tokens, i):
    pattern = re.compile(r':\s*\n')
    return pattern.search(tokens[i].all_string)


def count_dedents(tokens, i):
    res = 0
    if tokens[i].token_type == "DEDENT":
        res += 1
    j = 1
    while True:
        if tokens[i - j].token_type == "DEDENT":
            res += 1
            j += 1
        else:
            break
    return res


def find_last_module_element(tokens, i):
    j = 1
    while True:
        if (tokens[i - j].content != '\n'
                and tokens[i - j].token_type != "DEDENT"):
            return tokens[i - j]
        else:
            j += 1


def module_lines(tokens, length):
    if len(tokens) > length:
        return make_full_message(str(0), str(0), 'A0000')
    else:
        return ""


def line_break_bin_op(tokens, i, file_name):
    operators = ['+', '-', '*', '**', '/', '//', '%', '<<', '>>', '&', '|',
                 '^', '~', '<', '>', '<=', '>=', '==', '!=', '<>', '=', '+=',
                 '-=', '*=', '/=', '%=', '**=', '//=', 'not', 'and', 'or']
    if (tokens[i].content in operators
            and tokens[i + 1].content == '\n'
            and tokens[i - 1].content != "import"):
        return make_mes(tokens[i].start[0],
                        tokens[i].finish[1],
                        'A0006',
                        file_name)
    else:
        return ""


def check_list_args_indent(tokens, i, indent, file_name):
    res = []
    if (tokens[i].content == '['
            and tokens[i - 1].content == '='
            and tokens[i + 1].content != ']'):
        start_col = find_line_start(tokens, i)
        if tokens[i + 1].content == "\n":
            good_indent = start_col + indent
            j = 2
            br = 1
            while True:
                if tokens[i + j - 1].content == '\n':
                    if tokens[i + j].start[1] != good_indent:
                        if (tokens[i + j].content == ']'
                                and tokens[i + j].start[1] == start_col):
                            pass
                        else:
                            res.append(make_mes(tokens[i + j].start[0],
                                                tokens[i + j].start[1],
                                                'I0002',
                                                file_name))
                if tokens[i + j].content == '[':
                    br += 1
                elif tokens[i + j].content == ']':
                    br -= 1
                j += 1
                if br == 0:
                    break
        else:
            good_indent = tokens[i + 1].start[1]
            j = 2
            br = 1
            while True:
                if tokens[i + j - 1].content == '\n':
                    if tokens[i + j].start[1] != good_indent:
                        if (tokens[i + j].content == ']'
                                and tokens[i + j].start[1] == start_col):
                            pass
                        else:
                            res.append(make_mes(tokens[i + j].start[0],
                                                tokens[i + j].start[1],
                                                'I0002',
                                                file_name))
                if tokens[i + j].content == '[':
                    br += 1
                elif tokens[i + j].content == ']':
                    br -= 1
                j += 1
                if br == 0:
                    break
        return res


def check_func_args_indent(tokens, i, indent, file_name):
    res = []
    if tokens[i - 1].content == 'def':
        col_start = tokens[i - 1].start[1]
        if tokens[i + 2].content == '\n':
            good_indent = col_start + indent * 2
            j = 3
            br = 1
            while True:
                if tokens[i + j - 1].content == '\n':
                    if tokens[i + j].start[1] != good_indent:
                        if (tokens[i + j].content == ')'
                                and tokens[i + j].start[1] == col_start):
                            pass
                        else:
                            res.append(make_mes(tokens[i + j].start[0],
                                                tokens[i + j].start[1],
                                                'I0001',
                                                file_name))
                if tokens[i + j].content == '(':
                    br += 1
                elif tokens[i + j].content == ')':
                    br -= 1
                j += 1
                if br == 0:
                    break

        else:
            good_indent = tokens[i + 2].start[1]
            if tokens[i + 2].content == ')':
                pass
            else:
                j = 3
                br = 1
                while True:
                    if tokens[i + j - 1].content == '\n':
                        if tokens[i + j].start[1] != good_indent:
                            res.append(make_mes(tokens[i + j].start[0],
                                                tokens[i + j].start[1],
                                                'I0001',
                                                file_name))
                    if tokens[i + j].content == '(':
                        br += 1
                    elif tokens[i + j].content == ')':
                        br -= 1
                    j += 1
                    if br == 0:
                        break
    else:
        if tokens[i + 2].content == '\n':
            col_start = find_line_start(tokens, i)
            good_indent = col_start + indent
            j = 3
            br = 1
            while True:
                if br == 0:
                    break
                if tokens[i + j - 1].content == '\n':
                    if tokens[i + j].start[1] != good_indent:
                        if (tokens[i + j].content == ')'
                                and tokens[i + j].start[1] == col_start):
                            pass
                        else:
                            res.append(make_mes(tokens[i + j].start[0],
                                                tokens[i + j].start[1],
                                                'I0001',
                                                file_name))
                if tokens[i + j].content == ')':
                    br -= 1
                elif tokens[i + j].content == '(':
                    br += 1
                j += 1
        else:
            if is_function(tokens, i + 2):
                good_indent = tokens[i + 4]
                n = 2
            else:
                good_indent = tokens[i + 2].start[1]
                n = 0
            if tokens[i + 2 + n].content == ')':
                pass
            else:
                j = 3
                br = 1
                while True:
                    if tokens[i + j + n - 1].content == '\n':
                        if tokens[i + j + n].start[1] != good_indent:
                            res.append(make_mes(tokens[i + j + n].start[0],
                                                tokens[i + j + n].start[1],
                                                'I0001',
                                                file_name))
                    if tokens[i + j + n].content == '(':
                        br += 1
                    elif tokens[i + j + n].content == ')':
                        br -= 1
                    j += 1
                    if br == 0:
                        break
    return res


def find_line_start(tokens, i):
    j = 1
    types = ["ENC", "INDENT", "DEDENT", "NL"]
    while True:
        if tokens[i - j].token_type in types:
            res = tokens[i - j + 1].start[1]
            break
        else:
            j += 1
    return res


def find_line_start_e(tokens, i):
    j = 1
    flag = False
    types = ["ENC", "INDENT", "DEDENT", "NL"]
    while True:
        if tokens[i - j].token_type in types:
            if (tokens[i - j].token_type == "DEDENT"
                    and tokens[i - j].start[0] > tokens[i].start[0]):
                j += 1
                flag = True
            else:
                if flag and j == 2:
                    res = tokens[i]
                else:
                    res = tokens[i - j + 1]
                break
        else:
            j += 1
    return res


def check_trailing_space(tokens, i, file_name):
    if (tokens[i].content == '\n'
            and tokens[i - 1].finish[0] == tokens[i].start[0]):
        if tokens[i].start[1] - tokens[i - 1].finish[1] > 0:
            return make_mes(tokens[i].start[0],
                            tokens[i].start[1],
                                     'A0005',
                            file_name)
    return ""


def one_space_between_name_and_operator(tokens, i, file_name):
    keywords = ['assert', 'del', 'elif', 'except', 'for', 'in', 'is',
                'if', 'not', 'raise', 'return', 'while', 'yield']
    if tokens[i].token_type == "OP" and tokens[i - 1].token_type == "NAME" \
            and tokens[i - 1].token_type not in keywords \
            and tokens[i].content != '(' \
            and tokens[i].content not in keywords:
        if tokens[i].start[1] - tokens[i - 1].finish[1] > 1:
            return make_mes(tokens[i].start[0],
                            tokens[i].start[1],
                            'A0004',
                            file_name)
    return ""


def check_func_call_space(tokens, i, w, file_name):
    keywords = ['assert', 'del', 'elif', 'except', 'for', 'in',
                'if', 'not', 'raise', 'return', 'while', 'yield']
    if tokens[i].content in ['(', '['] \
            and tokens[i - 1].token_type == "NAME" \
            and tokens[i].start[0] == tokens[i - 1].start[0]:
        if w == 'yes':
            if tokens[i].start[1] - tokens[i - 1].finish[1] > 1:
                return make_mes(tokens[i].start[0],
                                tokens[i].start[1],
                                'A0003',
                                file_name)
            if tokens[i].start[1] == tokens[i - 1].finish[1]:
                return make_mes(tokens[i].start[0],
                                tokens[i].start[1],
                                'A0001',
                                file_name)
        elif w == 'no':
            space = 0
            if tokens[i - 1].content in keywords:
                space = 1
            if tokens[i].start[1] - tokens[i - 1].finish[1] != space:
                return make_mes(tokens[i].start[0],
                                tokens[i].start[1],
                                'A0002',
                                file_name)
    return ""


def ext_slice_colon_spaces(token, w, file_name):
    if w == 'yes':
        if (re.search(r'\[\s*\w*\s*:\s*\w*\s*\]', token.all_string)
                and not re.search(r'\[\s*\w*\s:\s\w*\s*\]', token.all_string)):
            return make_mes(token.start[0],
                            token.start[1],
                            'A0000',
                            file_name)
        elif (re.search(r'\[\s*\w*\s*:\s*\w*\s*:\s*\w*\s*\]', token.all_string)
                and not re.search(r'\[\s*\w*\s:\s\w*\s:\s\w*\s*\]',
                                  token.all_string)):
            return make_mes(token.start[0],
                            token.start[1],
                            'A0000',
                            file_name)

    elif w == 'no':
        if re.search(r'\[\s*\w*\s*:\s*\w*\s*\]', token.all_string) \
                and not re.search(r'\[\s*\w*:\w*\s*\]', token.all_string):
            return make_mes(token.start[0],
                            token.start[1],
                            'A0000',
                            file_name)
        elif re.search(r'\[\s*\w*\s*:\s*\w*\s*:\s*\w*\s*]', token.all_string) \
                and not re.search(r'\[\s*\w*:\w*:\w*\s*]', token.all_string):
            return make_mes(token.start[0],
                            token.start[1],
                            'A0000',
                            file_name)

    return ""


def line_is_long(token, length, file_name):
    if token.start[1] > length or token.finish[1] > length:
        return make_mes(token.start[0],
                        token.finish[1],
                        'C0301',
                        file_name)
    else:
        return ""


def docstr_line_is_long(token, length, file_name):
    start_col = token.start[1]
    lines = token.content.split('\n')
    if start_col + len(lines[0]) > length:
        return make_mes(token.start[0],
                        start_col + len(lines[0]),
                        'C0301',
                        file_name)
    for i in range(1, len(lines)):
        if len(lines[i]) > length:
            return make_mes(token.start[0] + i,
                            len(lines[i]),
                            'C0301',
                            file_name)
    return ""


def blank_line_in_the_end(tokens):
    line_number = str(tokens[-1].start[0])
    if tokens[-1].content != '\n' and tokens[-2].content != '\n':
        element_number = str(tokens[-2].finish[1])
        print(make_full_message(line_number, element_number, 'C0304'))


def check_white_spaces(tokens, i, file_name):
    res = []
    symbols = [':', ';', ',']
    pattern = re.compile(r'\[\s*\w*\s*:\s*\w*\s*(:\s*\w*\s*)?\]')
    match = pattern.search(tokens[i].all_string)

    if tokens[i].content == ':' and match:
        config = configparser.ConfigParser()
        config.read('config.ini')
        w = config['OPTIONAL']['ExtSliceColonSpaces']
        out = ext_slice_colon_spaces(tokens[i], w, file_name)
        if out:
            res.append(out)

    elif tokens[i].content in symbols:
        if ' ' + tokens[i].content in tokens[i].all_string:
            res.append(make_mes(tokens[i].start[0],
                                tokens[i].start[1] - 1,
                                'C0326',
                                file_name))

    closing_braces = ['}', ')', ']']
    opening_braces = ['{', '(', '[']
    if tokens[i].content in opening_braces:
        if tokens[i].content + ' ' in tokens[i].all_string:
            res.append(make_mes(tokens[i].start[0],
                                tokens[i].start[1],
                                'C0326',
                                file_name))

    elif tokens[i].content in closing_braces:
        if (' ' + tokens[i].content in tokens[i].all_string
                and tokens[i - 1].content != '\n'):
            if (tokens[i - 1].content == ','
                    and tokens[i - 1].finish[0] == tokens[i].start[0]
                    and tokens[i].start[1] - tokens[i - 1].finish[1] == 1):
                pass
            else:
                res.append(make_mes(tokens[i].start[0],
                                    tokens[i].start[1],
                                    'C0326',
                                    file_name))

    operators = ['==', '!=', '<>', '<=', '>=',
                 '<', '>', '=', '+=', '-=',
                 '*=', '**=', '/=', '//=', '&=',
                 '|=', '^=', '%=', '>>=', '<<=']
    if tokens[i].content in operators:
        if (tokens[i].content + ' ' not in tokens[i].all_string
                and ' ' + tokens[i].content not in tokens[i].all_string):
            res.append(make_mes(tokens[i].start[0],
                                tokens[i].start[1],
                                'C0326',
                                file_name))

    keywords = ['assert', 'del', 'elif', 'except', 'for', 'in', 'is',
                'if', 'not', 'raise', 'return', 'while', 'yield']
    if tokens[i].content in keywords:
        if (tokens[i].start[1] - tokens[i - 1].finish[1] > 1
                and tokens[i - 1].token_type != 'NL'):
            res.append(make_mes(tokens[i].start[0],
                                tokens[i].start[1],
                                'S0004',
                                file_name))
        if tokens[i + 1].start[1] - tokens[i].finish[1] > 1:
            res.append(make_mes(tokens[i].start[0],
                                tokens[i].start[1],
                                'S0005',
                                file_name))
    return res


def check_unnecessary_parentheses(tokens, i, file_name):
    keywords = ['assert', 'del', 'elif', 'except', 'for', 'in',
                'if', 'not', 'raise', 'return', 'while', 'yield']
    if tokens[i].content in keywords:
        if tokens[i + 1].content == '(':
            br = 1
            n = 2
            while True:
                if (tokens[i + n].content == ')'
                        and (tokens[i + n + 1].content == ':'
                             or tokens[i + n + 1].content == '\n')):
                    if tokens[i].content == 'except' and n > 3:
                        pass
                    elif tokens[i].start[0] != tokens[i + n].start[0]:
                        pass
                    else:
                        return make_mes(tokens[i + 1].start[0],
                                        tokens[i + 1].start[1],
                                        'C0325', file_name)
                if tokens[i + n].content == '(':
                    br += 1
                elif tokens[i + n].content == ')':
                    br -= 1
                if br == 0 and tokens[i + n].content == ':':
                    break
                n += 1
    return ""


def check_multiple_importing(tokens, i, file_name):
    if (tokens[i].content == 'import'
            and 'from' not in tokens[i].all_string
            and tokens[i + 2].content == ','
            and tokens[i + 3].token_type == "NAME"):
        return make_mes(tokens[i].start[0],
                        tokens[i].start[1],
                        'C0410',
                        file_name)


def check_star_importing(tokens, i, file_name):
    if tokens[i].content == 'import' and 'from' in tokens[i].all_string:
        if tokens[i + 1].content == '*':
            return make_mes(tokens[i + 1].start[0],
                            tokens[i + 1].start[1],
                            'A0007',
                            file_name)
    return ""


def check_several_statements(tokens, i, file_name):
    if tokens[i].content == ';' and tokens[i + 1].token_type == "NAME":
        line_number = tokens[i].start[0]
        element_number = tokens[i].start[1]
        return make_mes(line_number,
                        element_number,
                        'C0321',
                        file_name)


def check_trailing_semicolon(tokens, i, file_name):
    if tokens[i].content == ';' and tokens[i + 1].content == '\n':
        line_number = tokens[i].start[0]
        element_number = tokens[i].start[1]
        return make_mes(line_number,
                        element_number,
                        'C0305',
                        file_name)


def check_encoding(file_name, encoding):
    actual_encoding = get_encoding(file_name)
    if actual_encoding != encoding:
        print(make_message_line('0', 'E0501'))


def check_single_comments_pep8(tokens, i, file_name):
    res = []
    if tokens[i].token_type == "COMMENT":
        types = ["INDENT", "DEDENT", "ENC", "NL"]
        if (tokens[i - 1].token_type not in types
                and tokens[i].start[1] - tokens[i - 1].finish[1] < 2):
            res.append(make_mes(tokens[i].start[0],
                                tokens[i].start[1],
                                'S0001',
                                file_name))

        if tokens[i].content[1] != ' ':
            res.append(make_mes(tokens[i].start[0],
                                tokens[i].start[1],
                                'S0002',
                                file_name))
        elif tokens[i].content[2] == ' ':
            res.append(make_mes(tokens[i].start[0],
                                tokens[i].start[1],
                                'S0002',
                                file_name))
    return res


def check_multi_comments_pep8(tokens, i, file_name):
    lines = tokens[i].content.split('\n')
    if len(lines) == 2 and lines[1][-3:] == '\'\'\'':
        return make_mes(tokens[i].finish[0],
                        tokens[i].finish[1],
                        'A0008',
                        file_name)
    return ""


def check_multi_com_indent(tokens, i, file_name):
    j = 1
    res = tokens[i]
    while True:
        if tokens[i - j].token_type not in ['INDENT', 'DEDENT', 'NL', 'ENC']:
            res = tokens[i - j]
            break
        else:
            j += 1
    while True:
        if tokens[i - j].token_type in ['INDENT', 'DEDENT', 'NL', 'ENC']:
            res = tokens[i - j + 1]
            break
        else:
            j += 1
    if tokens[i].start[1] != res.start[1]:
        return make_mes(tokens[i].start[0],
                        tokens[i].start[1],
                        'A0009',
                        file_name)
    return ""


def check_is_multi_comment(tokens, i):
    return find_line_start_e(tokens, i) == tokens[i]


def check_type(tokens, i, t_type):
    return tokens[i].token_type == t_type


def check_eq_spaces_in_func(tokens, i, file_name):
    in_func = False
    in_func_2 = False
    if tokens[i - 1].token_type != "NAME":
        return "no"
    j = 2
    while True:
        try:
            if tokens[i - j].content == '\n':
                j += 1
            elif tokens[i - j].content == ',' or tokens[i - j].content == '(':
                in_func = True
                break
            elif (tokens[i - j].content == ':'
                  and tokens[i - j - 1].token_type == "NAME"):
                y = 2
                while True:
                    if tokens[i - j - y].content == '\n':
                        y += 1
                    elif (tokens[i - j - y].content == ','
                          or tokens[i - j - y].content == '('):
                        in_func_2 = True
                        break
                    else:
                        in_func_2 = False
                        break
                break
            else:
                in_func = False
                break
        except IndexError:
            return "no"
    if not in_func and not in_func_2:
        return "no"

    if in_func:
        if (tokens[i].start[1] - tokens[i - 1].finish[1] > 0
                and tokens[i + 1].start[1] - tokens[i].finish[1] > 0):
            return make_mes(tokens[i].start[0],
                            tokens[i].start[1],
                            'C0327',
                            file_name)
        else:
            return ""

    if in_func_2:
        if (tokens[i].start[1] - tokens[i - 1].finish[1] != 1
                and tokens[i + 1].start[1] - tokens[i].finish[1] != 1):
            return make_mes(tokens[i].start[0],
                            tokens[i].start[1],
                            'C0327',
                            file_name)
        else:
            return ""

    return "no"


def check_is_name_valid(tokens, i, file_name):
    invalid_names = ['l', 'O', 'I']
    if tokens[i].content in invalid_names:
        return make_mes(tokens[i].start[0],
                        tokens[i].start[1],
                        'N0001',
                        file_name)
    return ""


def is_ascii(tokens, i):
    if tokens[i].token_type == "NAME":
        if not all(ord(c) < 128 for c in tokens[i].content):
            return make_full_message(tokens[i].start[0],
                                     tokens[i].start[1],
                                     'N0002')
    return ""


def is_snake_case(tokens, i, file_name):
    word = tokens[i].content
    if len(word) == 1:
        return ""
    if tokens[i].content[:2] == tokens[i].content[-2:] == '__':
        word = tokens[i].content[2:-2]
    pattern = re.compile(r'\b_?[a-z]+[0-9]*(_?[0-9a-z]*)*_?\b')

    if not pattern.match(word):
        return make_mes(tokens[i].start[0],
                        tokens[i].start[1],
                        'N0003',
                        file_name)
    return ""


def is_camel_case(tokens, i, file_name):
    word = tokens[i].content
    pattern = re.compile(r'\b[a-zA-Z0-9]+\b')
    if not pattern.match(word) or (word == word.upper() and len(word) > 1):
        return make_mes(tokens[i].start[0],
                        tokens[i].start[1],
                        'N0004',
                        file_name)
    return ""


def is_upper_camel(tokens, i, file_name):
    word = tokens[i].content
    pattern = re.compile(r'\b([A-Z]+[a-z0-9]*)+\b')
    if not pattern.match(word) or word == word.upper():
        return make_mes(tokens[i].start[0],
                        tokens[i].start[1],
                        'N0005',
                        file_name)
    return ""


def check_func_spaces_1(tokens, i, lines, file_name):
    if tokens[i - 2].content == ':' or tokens[i - 1].token_type == "ENC":
        return ""
    j = 1
    flag = False
    nls = 0
    symbs = ['@', '#']
    try:
        while True:
            if tokens[i - j].content == '\n':
                j += 1
                nls += 1
            elif j == 3 and tokens[i - j].content == ':':
                flag = True
                break
            elif tokens[i - j].token_type == "INDENT" \
                    or tokens[i - j].token_type == "DEDENT":
                j += 1
            elif (tokens[i - j].all_string.lstrip()[0] in symbs
                  and tokens[i - j].start[0] - tokens[i].start[0] == -1):
                if tokens[i - j].content.lstrip()[0] in symbs:
                    nls -= 1
                j += 1
            else:
                break
    except IndexError:
        pass
    if not flag and nls - 1 != lines:
        return make_mes(tokens[i].start[0],
                        tokens[i].start[1],
                        'L0001',
                        file_name)
    return ""


def check_classes_spaces_before(tokens, i, lines, file_name):
    if tokens[i].content == 'class' and tokens[i].start[0] != 1:
        j = 1
        nls = 0
        try:
            while True:
                if tokens[i - j].content == '\n':
                    j += 1
                    nls += 1
                elif tokens[i - j].token_type == "INDENT" \
                        or tokens[i - j].token_type == "DEDENT":
                    j += 1
                else:
                    break
        except IndexError:
            pass
        if nls - 1 != lines:
            return make_mes(tokens[i].start[0],
                            tokens[i].start[1],
                            'L0002',
                            file_name)
        return ""


def check_classes_spaces_after(tokens, i, lines, file_name):
    if tokens[i].content != 'class' and tokens[i].token_type != 'DEDENT':
        nls = count_new_lines(tokens, i)
        if nls - 1 != lines:
            return make_mes(tokens[i].start[0],
                            tokens[i].start[1],
                            'L0002',
                            file_name)
    return ""


def count_new_lines(tokens, i):
    j = 1
    nls = 0
    try:
        while True:
            if tokens[i - j].content == '\n':
                j += 1
                nls += 1
            elif tokens[i - j].token_type == "INDENT" \
                    or tokens[i - j].token_type == "DEDENT":
                j += 1
            else:
                break
    except IndexError:
        pass
    return nls
