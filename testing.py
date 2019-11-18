from example import Tokenizer as tok
import string


class Tokens:
    eof = 'END-OF-FILE'
    name = 'NAME'
    number = 'NUMBER'
    operator = 'OP'
    keyword = 'KEYWORD'
    new_line = 'NL'
    comment = 'COMMENT'
    unknown = 'UNKNOWN'
    s_line = 'STRING'
    ind = 'INDENT'
    ded = 'DEDENT'

    keywords = ['assert', 'del', 'elif', 'except', 'for', 'in', 'is',
                'if', 'not', 'raise', 'return', 'while', 'yield']
    operators_w = ['and', 'or', 'not', 'in', 'is']
    operators = ['+', '-', '*', '**', '/', '//', '%', '<<', '>>', '&',
                 '|', '^', '~', '<', '>', '<=', '>=', '==', '!=', '<>',
                 '=', '+=', '-=', '*=', '/=', '%=', '**=', '//=',
                 '@', '!']
    quotes = ['\'', '\"']

    def __init__(self, tok_type, value, line, line_num, line_pos, start, end):
        self.tok_type = tok_type
        self.content = value
        self.line = line
        self.line_pos = line_pos - len(value)
        self.line_num = line_num
        self.start = start
        self.end = end

    def __str__(self):
        if self.content == '\n':
            self.content = '\\n'
        return '{0}:{1}'.format(self.line_num + 1, self.line_pos).ljust(10) \
               + self.tok_type.ljust(15) \
               + self.content.ljust(15) \
               + str(self.start).ljust(10) \
               + str(self.end).ljust(10) \
               + self.line

    def __repr__(self):
        return '{0}:{1}'.format(self.line_num + 1, self.line_pos).ljust(10) \
               + self.tok_type.ljust(15) + self.content


class Lexer:
    eof_marker = '$'
    comment = '#'

    def __init__(self, code):
        super(Lexer, self).__init__()

        self.code = code
        self.cursor = 0
        self.tokens = []

        self.lines = code.split('\n')
        self.line_no = 0
        self.line_pos = 0

    def get_next_char(self):
        self.cursor += 1
        self.line_pos += 1
        if self.cursor > len(self.code):
            return 'EOF'
        return self.code[self.cursor - 1]

    def get_prev_char(self):
        self.cursor -= 1
        self.line_pos -= 1
        return self.code[self.cursor - 1]

    @staticmethod
    def check_char(char):
        chars = [' ', '\n', '$'] + [*string.ascii_letters] + [*string.digits] + Tokens.operators + Tokens.quotes
        return char in chars

    def start_tokenize(self):
        unknown = ""
        self.line_pos = -1
        char = self.get_next_char()
        while char != 'EOF':

            if char == ' ':
                char = self.get_next_char()

            elif char == '\t':
                self.line_pos += 3
                char = self.get_next_char()

            elif char == '\n':
                start = (self.line_no, self.line_pos + 1)
                end = (self.line_no, self.line_pos + 2)
                token = Tokens(Tokens.new_line, char, self.lines[self.line_no],
                               self.line_no, self.line_pos + 1, start, end)
                self.tokens.append(token)
                self.line_no += 1
                self.line_pos = -1
                char = self.get_next_char()

            elif char == Lexer.comment:
                word = char
                while char != '\n':
                    char = self.get_next_char()
                    word += char
                start = (self.line_no, self.line_pos + 1)
                end = (self.line_no, self.line_pos + 1 + len(word))
                token = Tokens(Tokens.comment, word, self.lines[self.line_no],
                               self.line_no, self.line_pos + 1, start, end)
                self.tokens.append(token)

            elif char in string.ascii_letters + '_':
                word = char
                start = (self.line_no, self.line_pos)
                char = self.get_next_char()
                while char in (string.ascii_letters + string.digits + '_'):
                    word += char
                    char = self.get_next_char()
                end = (self.line_no, self.line_pos + len(word))
                token = Tokens(Tokens.name, word, self.lines[self.line_no],
                               self.line_no, self.line_pos, start, end)

                if word in Tokens.keywords:
                    token.tok_type = Tokens.keyword
                elif word in Tokens.operators_w:
                    token.tok_type = Tokens.operator

                self.tokens.append(token)

            elif char in string.digits:
                word = char
                start = (self.line_no, self.line_pos)
                end = (self.line_no, self.line_pos + len(word))
                char = self.get_next_char()
                while char in string.digits:
                    word += char
                    char = self.get_next_char()
                token = Tokens(Tokens.number, word, self.lines[self.line_no],
                               self.line_no, self.line_pos, start, end)
                self.tokens.append(token)

            elif char in '+-*/=<>:(){},.[]%@!&|^~':
                start = (self.line_no, self.line_pos + 1)
                end = (self.line_no, self.line_pos + 2)
                token = Tokens(Tokens.operator, char, self.lines[self.line_no],
                               self.line_no, self.line_pos + 1, start, end)
                self.tokens.append(token)
                char = self.get_next_char()

            elif char in Tokens.quotes:
                word = ""
                line_num = self.line_no
                elem = self.line_pos
                is_str_end = False
                while not is_str_end:
                    word += char
                    if char == '\n':
                        self.line_no += 1
                        self.line_pos = -1
                    char = self.get_next_char()
                    if char in Tokens.quotes and self.code[self.cursor - 2] != '\\':
                        is_str_end = True
                        word += char
                        char = self.get_next_char()
                token = Tokens(Tokens.s_line, word, self.lines[self.line_no],
                               line_num, elem + len(word))
                self.tokens.append(token)

            else:
                start = (self.line_no, self.line_pos)
                while not Lexer.check_char(char):
                    unknown += char
                    char = self.get_next_char()
                end = (self.line_no, self.line_pos)
                token = Tokens(Tokens.unknown, unknown, self.lines[self.line_no],
                               self.line_no, self.line_pos, start, end)
                self.tokens.append(token)
                unknown = ""

        token = Tokens(Tokens.eof, "", "", self.line_no + 1, 0,
                       (self.line_no + 1, 0), (self.line_no + 1, 0))
        self.tokens.append(token)

        return self.tokens

    def find_operators(self):
        tokens = self.tokens
        for i in range(len(tokens)):
            if tokens[i].tok_type == 'OP' and tokens[i + 1].tok_type == 'OP':
                op = tokens[i].content + tokens[i + 1].content
                if op in Tokens.operators:
                    tokens.pop(i + 1)
                    tokens[i].value = op
            if tokens[i].tok_type == Tokens.eof:
                break

    def find_multilines(self):
        try:
            tokens = self.tokens
            vals = ['\'\'', '\"\"']
            for i in range(len(tokens)):
                if tokens[i].content in vals \
                        and tokens[i + 2].value in vals \
                        and tokens[i + 1].tok_type == 'STRING':
                    res = tokens[i].content + tokens[i + 1].content + tokens[i + 2].content
                    tokens.pop(i + 1)
                    tokens.pop(i + 1)
                    tokens[i].value = res
        except IndexError:
            pass

    def find_dents(self):
        res = []
        tokens = self.tokens
        cur_indent = 0
        ind = 4
        for i in range(1, len(tokens)):
            if (tokens[i].line_num != tokens[i - 1].line_num
                    and tokens[i].line_pos // ind > cur_indent
                    and tokens[i - 1].line[-1:] == ':'):
                for j in range(tokens[i].line_pos // ind - cur_indent):
                    token = Tokens(Tokens.ind, "",
                                   self.lines[tokens[i].line_num],
                                   tokens[i].line_num,
                                   tokens[i].line_pos, (0, 0), (0, 0))
                    res.append(token)
                    cur_indent += 1
                res.append(tokens[i])
            elif (tokens[i].line_num != tokens[i - 1].line_num
                  and tokens[i].line_pos // ind < cur_indent
                  and tokens[i].line != ''):
                res.append(Tokens(Tokens.ded, "",
                                  self.lines[tokens[i].line_num],
                                  tokens[i].line_num,
                                  tokens[i].line_pos, (0, 0), (0, 0)))
                cur_indent -= 1
            else:
                res.append(tokens[i])
        self.tokens.clear()
        self.tokens.extend(res)


def write(tokens, file_name):
    f = open(file_name, 'w')
    for i in range(len(tokens)):
        f.write(str(i) + ' ' + str(tokens[i]) + '\n')
    f.close()


def main():
    code = tok.read1('test_files/tokens/indent.py')

    tok1 = Lexer(code)
    tokens = tok1.start_tokenize()
    for i in range(2):
        tok1.find_operators()
    tok1.find_multilines()
    tok1.find_dents()
    for token in tokens:
        print(token)
    write(tokens, 'write_test.txt')


if __name__ == '__main__':
    main()
