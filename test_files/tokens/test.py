a = [x for x in 'abcdefgh'] #['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
mylist = ['123', '234']

import configparser
from make_tokens import get_encoding


class Tokenizer(object):
    def __init__(self, token_type, content, start, finish, all_string):
        self.token_type = token_type
        self.content = content
        self.start = start
        self.finish = finish
        self.all_string = all_string


