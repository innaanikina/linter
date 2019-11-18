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
    def make_tokens1(file_name):
        s = Tokenizer.read1(file_name)
        return s

    @staticmethod
    def read1(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            return f.read()
