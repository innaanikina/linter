import configparser
from make_tokens import get_encoding


class Tokenizer(object):
    def __init__(self, token_type, content, start, finish, all_string):
        self.token_type = token_type
        self.content = content
        self.start = start
        self.finish = finish
        self.all_string = all_string

    def __str__(self):
        if self.content == '\n':
            token_content = '\\n'
        else:
            token_content = self.content
        return self.token_type \
               + ' ' + token_content \
               + ' ' + str(self.start) \
               + ' ' + str(self.finish) \
               + ' \"' + self.all_string[:-1] + '\"'

    @staticmethod
    def write_to_file(result, file_name):
        f = open(file_name, 'w')
        for i in range(len(result)):
            f.write(str(i) + ' ' + str(result[i]) + '\n')
        f.close()

    @staticmethod
    def make_token_objects(s):
        tokens = []
        string_tokens = Tokenizer.make_tokens(s)
        for token in string_tokens:
            tokens.append(Tokenizer(token[0], token[1],
                                    token[2], token[3], token[4]))
        return tokens

    @staticmethod
    def make_tokens(file_name):
        s = Tokenizer.reading(file_name)
        line = 1
        col = 0
        cur_line_content = []
        head = 0
        tail = 0
        word_list = []
        brackets = ['(', '[', '{', ')', ']', '}']
        quotes = ['\'', '\"']
        operators = ['+', '-', '*', '**', '/', '//', '%', '<<', '>>', '&',
                     '|', '^', '~', '<', '>', '<=', '>=', '==', '!=', '<>',
                     '=', '+=', '-=', '*=', '/=', '%=', '**=', '//=',
                     'not', 'and', 'or', '@', '!']
        operators1 = ['&', '|', '^', '~', '@']
        operators_d = {'+': '=', '-': '=', '*': '=', '/': '=',
                       '%': '=', '=': '=', '>': '>'}
        operators_w = ['and', 'or', 'not', 'in', 'is']
        op_list = []
        operator_is_started = False
        spaces = 0
        indent = Tokenizer.get_indent()
        indent_is_on = False
        counting_spaces = False
        indent_depth = 0
        line_num = 0
        col_num = 0
        f_ind = False
        com_started = False
        ignore = False

        result = []
        enc = get_encoding(file_name)
        Tokenizer.add_to_res(result, 0, "ENC", enc, (0, 0), (0, 0), "")
        words_counter = len(result)

        for i in range(len(s)):
            if ignore and line == line_num + 1:
                ignore = False
            if (col == 0 or counting_spaces) and s[i] == " ":
                spaces += 1
                counting_spaces = True
                if (s[i + 1] and s[i + 1] == '#'
                        and result[words_counter - 2][1] != ':'):
                    spaces = 0
                    counting_spaces = False
            elif (spaces > 0 and s[i] != " " and spaces % indent == 0
                  and s[i] != '\n' and s[i] != '#'):
                real_ind_depth = col // indent
                if f_ind and real_ind_depth > indent_depth:
                    q = real_ind_depth - indent_depth
                    start = col - q * indent
                    for x1 in range(0, q):
                        Tokenizer.add_to_res(result,
                                             words_counter,
                                             "INDENT",
                                             "",
                                             (line, start),
                                             (line, start + indent),
                                             "default")
                        words_counter += 1
                    indent_depth = col // indent
                    f_ind = False
                elif (real_ind_depth > indent_depth
                      and (result[words_counter - 1][1] == ':'
                           or result[words_counter - 2][1] == ':')):
                    q = real_ind_depth - indent_depth
                    start = col - q * indent
                    for x in range(q):
                        Tokenizer.add_to_res(result,
                                             words_counter,
                                             "INDENT",
                                             " " * indent,
                                             (line, start),
                                             (line, start + indent),
                                             "default")
                        words_counter += 1
                        start += indent
                    indent_is_on = True
                    indent_depth = col // indent
                elif real_ind_depth < indent_depth:
                    q = indent_depth - real_ind_depth
                    for x in range(q):
                        Tokenizer.add_to_res(result, words_counter,
                                             "DEDENT", "",
                                             (line, col), (line, col),
                                             "default")
                        words_counter += 1
                    indent_depth = col // indent
                counting_spaces = False
                spaces = 0
            elif (col == 0 and s[i] != " " and indent_is_on
                  and s[i] != '\n' and s[i] != '#'):
                for q in range(indent_depth):
                    Tokenizer.add_to_res(result,
                                         words_counter,
                                         "DEDENT",
                                         "",
                                         (line, col),
                                         (line, col),
                                         "default")
                    words_counter += 1
                indent_depth = col // indent
                indent_is_on = False
            elif (spaces > 0 and s[i] != " " and spaces % indent == 0
                  and s[i] != '\n' and s[i] == '#'
                  and result[words_counter - 2][1] == ':'):
                f_ind = True
                spaces = 0
                counting_spaces = False
            else:
                spaces = 0
                counting_spaces = False

            if s[i] == "#":
                if not word_list:
                    word_list.append(s[i])
                    line_num = line
                    col_num = col
                else:
                    word_list.append(s[i])

            elif word_list and word_list[0] == '#' and s[i] != '\n':
                word_list.append(s[i])

            elif word_list and word_list[0] in quotes:
                word_list.append(s[i])
                ln = len(word_list)
                if (ln == 2 and word_list and word_list[0] in quotes
                        and s[i] in quotes and s[i + 1] in quotes):
                    com_started = True
                    line_num = line
                    col_num = col - 1

                if (com_started and word_list[ln - 3] in quotes
                        and word_list[ln - 2] in quotes
                        and s[i] in quotes and ln > 3):
                    current_word = "".join(word_list)
                    word_list.clear()
                    Tokenizer.add_to_res(result,
                                         words_counter,
                                         "STRING",
                                         current_word,
                                         (line_num, col_num),
                                         (line, col + 1),
                                         "default")  # COM
                    words_counter = len(result)
                    com_started = False
                elif (s[i] == word_list[0]
                      and not com_started and s[i + 1] == s[i]):
                    pass
                elif s[i] == word_list[0] and not com_started:
                    current_word = "".join(word_list)
                    word_list.clear()
                    new_s_col = col + 1 - len(current_word)
                    Tokenizer.add_to_res(result,
                                         words_counter,
                                         "STRING",
                                         current_word,
                                         (line, new_s_col),
                                         (line, col + 1),
                                         "default")
                    words_counter = len(result)

            elif s[i] in operators:
                if word_list:
                    current_word = "".join(word_list)
                    word_list.clear()
                    if current_word in operators_w:
                        w_type = "OP"
                    elif Tokenizer.is_digit(current_word):
                        w_type = "NUMBER"
                    else:
                        w_type = "NAME"
                    Tokenizer.add_to_res(result,
                                         words_counter,
                                         w_type,
                                         current_word,
                                         (line, col - len(current_word)),
                                         (line, col),
                                         "default")
                    words_counter = len(result)
                if s[i] in operators1:
                    Tokenizer.add_to_res(result,
                                         words_counter,
                                         "OP",
                                         s[i],
                                         (line, col),
                                         (line, col + 1),
                                         "default")
                    words_counter += 1
                elif s[i] == '!' and not operator_is_started:
                    operator_is_started = True
                    op_list.append(s[i])
                elif (s[i] in operators_d.keys() or s[i] == '<') \
                        and not operator_is_started:
                    operator_is_started = True
                    op_list.append(s[i])
                elif (s[i] in ['<', '>', '=']
                      and operator_is_started and op_list[0] == '<'):
                    op_list.append(s[i])
                    current_word = "".join(op_list)
                    op_list.clear()
                    Tokenizer.add_to_res(result,
                                         words_counter,
                                         "OP",
                                         current_word,
                                         (line, col - 1),
                                         (line, col + 1),
                                         "default")
                    words_counter += 1
                    operator_is_started = False

                elif (operator_is_started
                      and op_list[0] == '!' and s[i] == '='):
                    op_list.append(s[i])
                    current_word = "".join(op_list)
                    op_list.clear()
                    Tokenizer.add_to_res(result,
                                         words_counter,
                                         "OP",
                                         current_word,
                                         (line, col - 1),
                                         (line, col + 1),
                                         "default")
                    words_counter += 1
                    operator_is_started = False

                elif (operator_is_started
                      and s[i] in ['*', '/'] and s[i] == op_list[0]):
                    op_list.append(s[i])

                elif (operator_is_started
                      and len(op_list) == 2 and s[i] == '='):
                    op_list.append(s[i])
                    current_word = "".join(op_list)
                    op_list.clear()
                    Tokenizer.add_to_res(result,
                                         words_counter,
                                         "OP",
                                         current_word,
                                         (line, col - 2),
                                         (line, col + 1),
                                         "default")
                    words_counter += 1
                    operator_is_started = False

                elif s[i] in operators_d.values() and operator_is_started:
                    op_list.append(s[i])
                    current_word = "".join(op_list)
                    op_list.clear()
                    Tokenizer.add_to_res(result,
                                         words_counter,
                                         "OP",
                                         current_word,
                                         (line, col - 1),
                                         (line, col + 1),
                                         "default")
                    words_counter += 1
                    operator_is_started = False

            elif s[i] in brackets or s[i] in ['\n', '.', ',', ':', ';']:
                if op_list and operator_is_started:
                    current_word = "".join(op_list)
                    op_list.clear()
                    new_col = col - len(current_word)
                    Tokenizer.add_to_res(result,
                                         words_counter,
                                         "OP",
                                         current_word,
                                         (line, new_col),
                                         (line, col), "default")
                    words_counter += 1
                    operator_is_started = False
                elif word_list:
                    if word_list[0] == '#':
                        current_word = "".join(word_list)
                        word_list.clear()
                        new_col = col_num + len(current_word)
                        Tokenizer.add_to_res(result,
                                             words_counter,
                                             "COMMENT",
                                             current_word,
                                             (line_num, col_num),
                                             (line_num, new_col),
                                             "default")
                        words_counter += 1
                    else:
                        current_word = "".join(word_list)
                        word_list.clear()
                        if current_word in operators_w:
                            w_type = "OP"
                        elif Tokenizer.is_digit(current_word):
                            w_type = "NUMBER"
                        else:
                            w_type = "NAME"
                        Tokenizer.add_to_res(result,
                                             words_counter,
                                             w_type,
                                             current_word,
                                             (line, col - len(current_word)),
                                             (line, col),
                                             "default")
                        words_counter = len(result)
                if s[i] == '\n':
                    w_type = 'NL'
                else:
                    w_type = 'OP'
                if s[i] == '\n' and not ignore or s[i] != '\n':
                    Tokenizer.add_to_res(result,
                                         words_counter,
                                         w_type,
                                         s[i],
                                         (line, col),
                                         (line, col + 1),
                                         "default")
                    words_counter += 1

                if s[i] == '\n':
                    cur_line_content.append(s[i])
                    cur_line = "".join(cur_line_content)
                    if line != 1:
                        head = tail
                    tail = words_counter
                    for z in range(head, tail):
                        result[z][4] = cur_line

                    cur_line_content.clear()
                    line += 1
                    col = -1

            elif s[i] != " ":
                if op_list and operator_is_started:
                    current_word = "".join(op_list)
                    op_list.clear()
                    Tokenizer.add_to_res(result,
                                         words_counter,
                                         "OP",
                                         current_word,
                                         (line, col - len(current_word)),
                                         (line, col),
                                         "default")
                    words_counter += 1
                    operator_is_started = False
                elif s[i] == '\\':
                    ignore = True
                    line_num = line
                if not ignore:
                    word_list.append(s[i])

            elif s[i] == ' ':
                if op_list and operator_is_started:
                    current_word = "".join(op_list)
                    op_list.clear()
                    Tokenizer.add_to_res(result,
                                         words_counter,
                                         "OP",
                                         current_word,
                                         (line, col - len(current_word)),
                                         (line, col),
                                         "default")
                    words_counter += 1
                    operator_is_started = False

                if word_list:
                    current_word = "".join(word_list)
                    if current_word in operators_w:
                        w_type = "OP"
                    elif Tokenizer.is_digit(current_word):
                        w_type = "NUMBER"
                    else:
                        w_type = "NAME"
                    Tokenizer.add_to_res(result,
                                         words_counter,
                                         w_type,
                                         current_word,
                                         (line, col - len(current_word)),
                                         (line, col),
                                         "default")
                    words_counter = len(result)
                    word_list.clear()

            if s[i] != '\n':
                cur_line_content.append(s[i])

            if com_started and s[i] == '\n':
                line += 1
                col = -1

            if i == len(s) - 1 and cur_line_content:
                cur_line = "".join(cur_line_content)
                if line != 0:
                    head = tail
                tail = words_counter
                for z in range(head, tail):
                    result[z][4] = cur_line
            col += 1

        Tokenizer.add_to_res(result,
                             words_counter,
                             "EOF",
                             "",
                             (line, 0),
                             (line, 0),
                             "")
        return result

    @staticmethod
    def reading(file_name):
        s = ""
        with open(file_name, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                s += line
        return s

    @staticmethod
    def make_token_words(file):
        lines = file.split("\n")
        for line in lines:
            words = line.split()
            words.append("\n")
            line += "\n"
        return lines

    @staticmethod
    def get_indent():
        config = configparser.ConfigParser()
        config.read('config.ini')
        indent = 4
        return indent

    @staticmethod
    def is_digit(e):
        if e.isdigit():
            return True
        else:
            try:
                float(e)
                return True
            except ValueError:
                return False

    @staticmethod
    def add_to_res(res, i, val_1, val_2, val_3, val_4, val_5):
        res.append([])
        for v in range(5):
            res[i].append("default")
        res[i][0] = val_1
        res[i][1] = val_2
        res[i][2] = val_3
        res[i][3] = val_4
        res[i][4] = val_5
