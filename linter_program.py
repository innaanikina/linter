# -*- coding: utf-8 -*-

import sys
import os
import configparser
import checkers as ch
from tokenizer import Tokenizer
from make_tokens import is_function, is_func_decl, \
    is_class_decl, get_class_start, is_end
from message import make_mes


def check_tokens(tokens):
    result = []
    for i in range(len(tokens)):
        result.append([])
        result[i].append(tokens[i].token_type)
        result[i].append(tokens[i].content)
        result[i].append(tokens[i].start)
        result[i].append(tokens[i].finish)
        result[i].append(tokens[i].all_string)
    Tokenizer.write_to_file(result, 'output.txt')
    print(result)


def main(conf_f, file):
    print(file)

    line = 0
    module_content = []
    mod_lvl = -1
    checked = False
    tokens = Tokenizer.make_token_objects(file)

    class_started = False
    class_start = (-1, -1)

    end = False

    conf = configparser.ConfigParser()
    conf.read(conf_f)
    encoding = conf['DEFAULT']['Encoding']
    indent = 4

    if encoding != '':
        ch.check_encoding(file, encoding)

    Tokenizer.write_to_file(tokens, 'test.txt')

    for i in range(len(tokens)):
        if (tokens[i].content == '='
                and conf['DEFAULT']['FuncArgEqNoSpace'] == 'yes'):
            out = ch.check_eq_spaces_in_func(tokens, i, file)
            if out != "" and out != "no":
                print(out)
                checked = True
            elif out != "no":
                checked = True

        if is_function(tokens, i):
            if conf['OPTIONAL']['Pep8FuncArgs'] == 'yes':
                out = ch.check_func_args_indent(tokens, i, indent, file)
                if out:
                    for s in out:
                        print(s)

        if conf['OPTIONAL']['Pep8ListArgs'] == 'yes':
            out = ch.check_list_args_indent(tokens, i, indent, file)
            if out:
                for s in out:
                    print(s)

        if conf['DEFAULT']['LineBreakAfterBinOp'] == 'no':
            check_pr(ch.line_break_bin_op(tokens, i, file))

        if conf['DEFAULT']['StarImport'] == 'no':
            check_pr(ch.check_star_importing(tokens, i, file))

        if conf['DEFAULT']['OneImportAtATime'] == 'yes':
            check_pr(ch.check_multiple_importing(tokens, i, file))

        if conf['DEFAULT']['WhiteSpaces'] == 'yes' and not checked:
            out = ch.check_white_spaces(tokens, i, file)
            if out:
                for s in out:
                    print(s)

        if conf['DEFAULT']['ParenthesesAroundKeywords'] == 'no':
            check_pr(ch.check_unnecessary_parentheses(tokens, i, file))

        if conf['DEFAULT']['SeveralStatementsInLine'] == 'no':
            check_pr(ch.check_several_statements(tokens, i, file))

        if conf['DEFAULT']['TrailingSemicolon'] == 'no':
            check_pr(ch.check_trailing_semicolon(tokens, i, file))

        if conf['DEFAULT']['MaxLineLength'] != 'no' \
                and tokens[i].start[0] != line:
            if tokens[i].token_type == "COMMENT":
                length = int(conf['DEFAULT']['MaxLineDocCom'])
                out = ch.line_is_long(tokens[i], length, file)
            elif tokens[i].token_type == "COM":
                length = int(conf['DEFAULT']['MaxLineDocCom'])
                out = ch.docstr_line_is_long(tokens[i], length)
            else:
                length = int(conf['DEFAULT']['MaxLineLength'])
                out = ch.line_is_long(tokens[i], length, file)
            if out != "":
                line = tokens[i].start[0]
                print(out)

        if conf['SPACES']['FuncCallSpace'] != '-':
            check_pr(ch.check_func_call_space(tokens, i,
                                              conf['SPACES']['FuncCallSpace'],
                                              file))

        if conf['DEFAULT']['SpacesBetweenNameAndOperator'] == str(1):
            check_pr(ch.one_space_between_name_and_operator(tokens, i, file))

        if conf['DEFAULT']['TrailingSpace'] == 'no':
            check_pr(ch.check_trailing_space(tokens, i, file))

        if conf['COMMENTS']['Pep8SingleComs'] == 'yes':
            out = ch.check_single_comments_pep8(tokens, i, file)
            if out:
                for s in out:
                    print(s)

        if conf['COMMENTS']['Pep8MultiComs'] == 'yes':
            if (tokens[i].token_type == "STRING"
                    and len(tokens[i].content) > 6
                    and tokens[i].content[0] == tokens[i].content[1]
                    == tokens[i].content[2] in ['\'', '\"']):
                if ch.check_is_multi_comment(tokens, i):
                    check_pr(ch.check_multi_comments_pep8(tokens, i, file))
                    check_pr(ch.check_multi_com_indent(tokens, i, file))

        if conf['OPTIONAL']['MaxModuleLines'] != 'no':
            modules = ['def', 'if', 'for', 'elif', 'else',
                       'while', 'try', 'except', 'class']
            if tokens[i].token_type == "EOF" and mod_lvl > -1:
                e = ch.find_last_module_element(tokens, i)
                for j in range(len(module_content)):
                    lines = e.start[0] - module_content[mod_lvl][0] + 1
                    length = int(conf['OPTIONAL']['MaxModuleLines'])
                    if lines > length:
                        print(make_mes(e.finish[0],
                                       e.finish[1],
                                       'L0003', file)
                              + ' ' + module_content[mod_lvl][2])
                    mod_lvl -= 1
                    module_content.pop()
            if (mod_lvl > -1 and tokens[i].token_type == "DEDENT"
                    and tokens[i + 1].token_type != "DEDENT"
                    and (tokens[i].start[1] == module_content[mod_lvl][1]
                         or (module_content[mod_lvl][1]
                             - tokens[i].start[1]) % indent == 0)):
                r1 = ch.count_dedents(tokens, i)
                e = ch.find_last_module_element(tokens, i)
                for j in range(r1):
                    lines = e.start[0] - module_content[mod_lvl][0] + 1
                    length = int(conf['OPTIONAL']['MaxModuleLines'])
                    if lines > length:
                        print(make_mes(e.finish[0],
                                       e.finish[1],
                                       'L0003',
                                       file)
                              + ' ' + module_content[mod_lvl][2])
                    mod_lvl -= 1
                    module_content.pop()

            if tokens[i].content in modules:
                mod_lvl += 1
                module_content.append([])
                module_content[mod_lvl].append(tokens[i].start[0])
                module_content[mod_lvl].append(tokens[i].start[1])
                module_content[mod_lvl].append(tokens[i].content)

        checked = False

        if conf['NAMES']['CheckForbNames'] == 'yes':
            check_pr(ch.check_is_name_valid(tokens, i, file))

        if conf['NAMES']['FuncCase'] == 'snake':
            if is_func_decl(tokens, i):
                check_pr(ch.is_snake_case(tokens, i, file))

        if conf['NAMES']['FuncCase'] == 'camel':
            if is_func_decl(tokens, i):
                check_pr(ch.is_camel_case(tokens, i, file))

        if conf['NAMES']['VarNames'] == 'snake':
            if (tokens[i].token_type == "NAME"
                    and tokens[i + 1].content == "="):
                check_pr(ch.is_snake_case(tokens, i, file))

        if conf['NAMES']['VarNames'] == 'camel':
            if (tokens[i].token_type == "NAME"
                    and tokens[i + 1].content == "="):
                check_pr(ch.is_camel_case(tokens, i, file))

        if conf['NAMES']['ClassNames'] == 'ucamel':
            if is_class_decl(tokens, i):
                check_pr(ch.is_upper_camel(tokens, i, file))

        if conf['NAMES']['ClassNames'] == 'camel':
            if is_class_decl(tokens, i):
                check_pr(ch.is_camel_case(tokens, i, file))

        if conf['NAMES']['ClassNames'] == 'snake':
            if is_class_decl(tokens, i):
                check_pr(ch.is_snake_case(tokens, i, file))

        if conf['SPACES']['SpacesBetwFuncsInClass'] != 'no':
            spaces = int(conf['SPACES']['SpacesBetwFuncsInClass'])
            if not class_started and get_class_start(tokens, i) != (-1, -1):
                class_started = True
                class_start = get_class_start(tokens, i)
            elif class_started and is_end(tokens, i, class_start):
                end = True
                class_started = False

            if class_started and tokens[i].content == 'def':
                check_pr(ch.check_func_spaces_1(tokens, i, spaces, file))

        if conf['SPACES']['SpacesBetwFuncNotInClass'] != 'no':
            ext_spaces = int(conf['SPACES']['SpacesBetwFuncNotInClass'])
            if not class_started and tokens[i].content == 'def':
                check_pr(ch.check_func_spaces_1(tokens, i, ext_spaces, file))

        if conf['SPACES']['SpacesBetwClasses'] != 'no':
            cl_spaces = int(conf['SPACES']['SpacesBetwClasses'])
            check_pr(ch.check_classes_spaces_before(tokens, i,
                                                    cl_spaces, file))
            if end and not tokens[i].token_type == 'EOF':
                check_pr(ch.check_classes_spaces_after(tokens, i,
                                                       cl_spaces, file))
                if not tokens[i].token_type == 'DEDENT':
                    end = False

    if conf['DEFAULT']['EndLine'] == 'yes':
        check_pr(ch.blank_line_in_the_end(tokens, file))


def check_pr(out):
    if out:
        print(out)


if __name__ == "__main__":
    args = []
    if len(sys.argv) < 3:
        print('\nПример запуска программы: linter_program.py'
              + ' config.ini file1.py file2.py')
    elif len(sys.argv) > 2:
        conf_file = sys.argv[1]
        for e in range(2, len(sys.argv)):
            args.append(sys.argv[e])
        try:
            for ar in args:
                if os.path.isdir(ar):
                    for root, dirs, args in os.walk(ar):
                        for file1 in args:
                            if (file1.endswith(".py")
                                    and file1 != '__init__.py'):
                                my_file = os.path.join(root, file1)
                                main(conf_file, my_file)
                else:
                    main(conf_file, ar)
        except FileNotFoundError:
            print('Ошибка! Файл не найден: ' + ar)
        except PermissionError:
            print("Ошибка доступа")
