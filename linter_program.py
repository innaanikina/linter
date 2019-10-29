from checkers import check_multiple_importing, check_white_spaces, \
    check_unnecessary_parentheses, check_several_statements, \
    check_trailing_semicolon, blank_line_in_the_end, line_is_long, check_encoding, docstr_line_is_long, \
    check_func_call_space, one_space_between_name_and_operator, check_trailing_space, check_func_args_indent, \
    check_list_args_indent, line_break_bin_op, check_star_importing, check_single_comments_pep8, \
    find_last_module_element, count_dedents, check_multi_comments_pep8, check_is_multi_comment, \
    check_multi_com_indent, check_eq_spaces_in_func, check_is_name_valid, is_snake_case, is_camel_case, is_upper_camel, \
    check_func_spaces_1, check_classes_spaces_before, check_classes_spaces_after
import configparser
from tokenizer import Tokenizer
from make_tokens import is_function, is_func_decl, is_class_decl, get_class_start, is_end
from message import make_mes
import sys
import os


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


def main(conf_file, file):
    print(file)

    line = 0
    module_content = []
    mod_lvl = -1
    checked = False
    tokens = Tokenizer.make_token_objects(file)

    class_started = False
    class_start = (-1, -1)

    end = False

    config = configparser.ConfigParser()
    config.read(conf_file)
    encoding = config['DEFAULT']['Encoding']
    indent = 4

    if encoding != '':
        check_encoding(file, encoding)

    Tokenizer.write_to_file(tokens, 'test.txt')

    for i in range(len(tokens)):
        if tokens[i].content == '=' and config['DEFAULT']['FuncArgEqNoSpace'] == 'yes':
            out = check_eq_spaces_in_func(tokens, i, file)
            if out != "" and out != "no":
                print(out)
                checked = True
            elif out != "no":
                checked = True

        if is_function(tokens, i):
            if config['OPTIONAL']['Pep8FuncArgs'] == 'yes':
                out = check_func_args_indent(tokens, i, indent, file)
                if out:
                    for s in out:
                        print(s)

        if config['OPTIONAL']['Pep8ListArgs'] == 'yes':
            out = check_list_args_indent(tokens, i, indent, file)
            if out:
                for s in out:
                    print(s)

        if config['DEFAULT']['LineBreakAfterBinOp'] == 'no':
            check_print(line_break_bin_op(tokens, i, file))

        if config['DEFAULT']['StarImport'] == 'no':
            check_print(check_star_importing(tokens, i, file))

        if config['DEFAULT']['OneImportAtATime'] == 'yes':
            check_print(check_multiple_importing(tokens, i, file))

        if config['DEFAULT']['WhiteSpaces'] == 'yes' and not checked:
            out = check_white_spaces(tokens, i, file)
            if out:
                for s in out:
                    print(s)

        if config['DEFAULT']['ParenthesesAroundKeywords'] == 'no':
            check_print(check_unnecessary_parentheses(tokens, i, file))

        if config['DEFAULT']['SeveralStatementsInLine'] == 'no':
            check_print(check_several_statements(tokens, i, file))

        if config['DEFAULT']['TrailingSemicolon'] == 'no':
            check_print(check_trailing_semicolon(tokens, i, file))

        if config['DEFAULT']['MaxLineLength'] != 'no' \
                and tokens[i].start[0] != line:
            if tokens[i].token_type == "COMMENT":
                length = int(config['DEFAULT']['MaxLineDocCom'])
                out = line_is_long(tokens[i], length, file)
            elif tokens[i].token_type == "COM":
                length = int(config['DEFAULT']['MaxLineDocCom'])
                out = docstr_line_is_long(tokens[i], length)
            else:
                length = int(config['DEFAULT']['MaxLineLength'])
                out = line_is_long(tokens[i], length, file)
            if out != "":
                line = tokens[i].start[0]
                print(out)

        if config['SPACES']['FuncCallSpace'] != '-':
            check_print(check_func_call_space(tokens, i, config['SPACES']['FuncCallSpace'], file))

        if config['DEFAULT']['SpacesBetweenNameAndOperator'] == str(1):
            check_print(one_space_between_name_and_operator(tokens, i, file))

        if config['DEFAULT']['TrailingSpace'] == 'no':
            check_print(check_trailing_space(tokens, i, file))

        if config['COMMENTS']['Pep8SingleComs'] == 'yes':
            out = check_single_comments_pep8(tokens, i, file)
            if out:
                for s in out:
                    print(s)

        if config['COMMENTS']['Pep8MultiComs'] == 'yes':
            if tokens[i].token_type == "STRING" \
                and len(tokens[i].content) > 6 \
                    and tokens[i].content[0] == tokens[i].content[1] == tokens[i].content[2] in ['\'', '"']:
                    if check_is_multi_comment(tokens, i):
                        check_print(check_multi_comments_pep8(tokens, i, file))
                        check_print(check_multi_com_indent(tokens, i, file))

        if config['OPTIONAL']['MaxModuleLines'] != 'no':
            modules = ['def', 'if', 'for', 'elif', 'else',
                       'while', 'try', 'except', 'class']
            if tokens[i].token_type == "EOF" and mod_lvl > -1:
                e = find_last_module_element(tokens, i)
                for j in range(len(module_content)):
                    lines = e.start[0] - module_content[mod_lvl][0] + 1
                    length = int(config['OPTIONAL']['MaxModuleLines'])
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
                         or (module_content[mod_lvl][1] - tokens[i].start[1]) % indent == 0)):
                r1 = count_dedents(tokens, i)
                e = find_last_module_element(tokens, i)
                for j in range(r1):
                    lines = e.start[0] - module_content[mod_lvl][0] + 1
                    length = int(config['OPTIONAL']['MaxModuleLines'])
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

        if config['NAMES']['CheckForbNames'] == 'yes':
            check_print(check_is_name_valid(tokens, i, file))

        if config['NAMES']['FuncCase'] == 'snake':
            if is_func_decl(tokens, i):
                check_print(is_snake_case(tokens, i, file))

        if config['NAMES']['FuncCase'] == 'camel':
            if is_func_decl(tokens, i):
                check_print(is_camel_case(tokens, i, file))

        if config['NAMES']['VarNames'] == 'snake':
            if tokens[i].token_type == "NAME" and tokens[i + 1].content == "=":
                check_print(is_snake_case(tokens, i, file))

        if config['NAMES']['VarNames'] == 'camel':
            if tokens[i].token_type == "NAME" and tokens[i + 1].content == "=":
                check_print(is_camel_case(tokens, i, file))

        if config['NAMES']['ClassNames'] == 'ucamel':
            if is_class_decl(tokens, i):
                check_print(is_upper_camel(tokens, i, file))

        if config['NAMES']['ClassNames'] == 'camel':
            if is_class_decl(tokens, i):
                check_print(is_camel_case(tokens, i, file))

        if config['NAMES']['ClassNames'] == 'snake':
            if is_class_decl(tokens, i):
                check_print(is_snake_case(tokens, i, file))

        if config['SPACES']['SpacesBetwFuncsInClass'] != 'no':
            spaces = int(config['SPACES']['SpacesBetwFuncsInClass'])
            if not class_started and get_class_start(tokens, i) != (-1, -1):
                class_started = True
                class_start = get_class_start(tokens, i)
            elif class_started and is_end(tokens, i, class_start):
                end = True
                class_started = False

            if class_started and tokens[i].content == 'def':
                check_print(check_func_spaces_1(tokens, i, spaces, file))

        if config['SPACES']['SpacesBetwFuncNotInClass'] != 'no':
            ext_spaces = int(config['SPACES']['SpacesBetwFuncNotInClass'])
            if not class_started and tokens[i].content == 'def':
                check_print(check_func_spaces_1(tokens, i, ext_spaces, file))

        if config['SPACES']['SpacesBetwClasses'] != 'no':
            cl_spaces = int(config['SPACES']['SpacesBetwClasses'])
            check_print(check_classes_spaces_before(tokens, i, cl_spaces, file))
            if end and not tokens[i].token_type == 'EOF':
                check_print(check_classes_spaces_after(tokens, i, cl_spaces, file))
                if not tokens[i].token_type == 'DEDENT':
                    end = False

    if config['DEFAULT']['EndLine'] == 'yes':
        blank_line_in_the_end(tokens)


def check_print(out):
    if out:
        print(out)


if __name__ == "__main__":
    files = []
    if len(sys.argv) < 3:
        print('\nПример запуска программы: linter_program.py' +
              ' config.ini file1.py file2.py')
    elif len(sys.argv) > 2:
        conf_file = sys.argv[1]
        for e in range(2, len(sys.argv)):
            files.append(sys.argv[e])
        try:
            for file in files:
                if os.path.isdir(file):
                    print("this is a directory")
                else:
                    main(conf_file, file)
        except FileNotFoundError:
            print('Ошибка! Файл не найден: ' + file)
        except PermissionError:
            print("Ошибка доступа")
