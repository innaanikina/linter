from chekers import check_multiple_importing, check_white_spaces, \
    check_unnecessary_parentheses, check_several_statements, \
    check_trailing_semicolon, blank_line_in_the_end, line_is_long, check_encoding, docstr_line_is_long, \
    check_func_call_space, one_space_between_name_and_operator, check_trailing_space, check_func_args_indent, \
    check_list_args_indent, line_break_bin_op, check_star_importing, check_single_comments_pep8, \
    find_last_module_element, count_dedents, check_correct_module, check_multi_comments_pep8, check_is_multi_comment, \
    check_multi_com_indent, check_eq_spaces_in_func, check_is_name_valid, is_snake_case, is_camel_case, is_upper_camel, \
    check_func_spaces_1
import configparser
from tokenizer import Tokenizer
from make_tokens import is_function, tokenize_file, read_file, is_func_decl, is_class_decl, get_class_start, is_end


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


def main():
    line = 0
    module_content = []
    mod_lvl = -1
    checked = False
    tokens = Tokenizer.make_token_objects('example.py')

    class_started = False
    class_start = (-1, -1)

    check_tokens(tokens)

    config = configparser.ConfigParser()
    config.read('config.ini')
    encoding = config['DEFAULT']['Encoding']
    indent = int(config['DEFAULT']['Indent'])

    if encoding != '':
        check_encoding('example.py', encoding)

    for i in range(len(tokens)):
        if tokens[i].content == '=' and config['DEFAULT']['FuncArgEqNoSpace'] == 'yes':
            out = check_eq_spaces_in_func(tokens, i)
            if out != "" and out != "no":
                print(out)
                checked = True
            elif out != "no":
                checked = True

        if is_function(tokens, i):
            if config['OPTIONAL']['Pep8FuncArgs'] == 'yes':
                check_func_args_indent(tokens, i, indent)  # сделать нормальный вывод, с return

        if config['OPTIONAL']['Pep8ListArgs'] == 'yes':
            check_list_args_indent(tokens, i, indent)

        if config['DEFAULT']['LineBreakAfterBinOp'] == 'no':
            out = line_break_bin_op(tokens, i)
            if out != "":
                print(out)

        if config['DEFAULT']['StarImport'] == 'no':
            out = check_star_importing(tokens, i)
            if out != "":
                print(out)

        if config['DEFAULT']['OneImportAtATime'] == 'yes':
            check_multiple_importing(tokens, i)
        if config['DEFAULT']['WhiteSpaces'] == 'yes' and not checked:
            check_white_spaces(tokens, i)
        if config['DEFAULT']['ParenthesesAroundKeywords'] == 'no':
            check_unnecessary_parentheses(tokens, i)
        if config['DEFAULT']['SeveralStatementsInLine'] == 'no':
            check_several_statements(tokens, i)
        if config['DEFAULT']['TrailingSemicolon'] == 'no':
            check_trailing_semicolon(tokens, i)

        if config['DEFAULT']['MaxLineLength'] != 'no' and tokens[i].start[0] != line:
            if tokens[i].token_type == "COMMENT":
                length = int(config['DEFAULT']['MaxLineDocCom'])
                out = line_is_long(tokens[i], length)
            elif tokens[i].token_type == "COM":
                length = int(config['DEFAULT']['MaxLineDocCom'])
                out = docstr_line_is_long(tokens[i], length)
            else:
                length = int(config['DEFAULT']['MaxLineLength'])
                out = line_is_long(tokens[i], length)
            if out != "":
                line = tokens[i].start[0]
                print(out)

        if config['SPACES']['FuncCallSpace'] != '-':
            out = check_func_call_space(tokens, i, config['SPACES']['FuncCallSpace'])
            if out != "":
                print(out)

        if config['DEFAULT']['SpacesBetweenNameAndOperator'] == str(1):
            out = one_space_between_name_and_operator(tokens, i)
            if out != "":
                print(out)

        if config['DEFAULT']['TrailingSpace'] == 'no':
            out = check_trailing_space(tokens, i)
            if out != "":
                print(out)

        if config['COMMENTS']['Pep8SingleComs'] == 'yes':
            check_single_comments_pep8(tokens, i)

        if config['COMMENTS']['Pep8MultiComs'] == 'yes':
            if tokens[i].token_type == "STRING" \
                and len(tokens[i].content) > 6 \
                    and tokens[i].content[0] == tokens[i].content[1] == tokens[i].content[2] in ['\'', '"']:
                    if check_is_multi_comment(tokens, i):
                        out = check_multi_comments_pep8(tokens, i)
                        if out:
                            print(out)
                            out = ""
                        out = check_multi_com_indent(tokens, i)
                        if out != "":
                            print(out)

        if config['OPTIONAL']['MaxModuleLines'] != 'no':
            modules = ['def', 'if', 'for', 'elif', 'else', 'while', 'try', 'except', 'class']
            if tokens[i].token_type == "EOF" and mod_lvl > -1:
                e = find_last_module_element(tokens, i)
                for j in range(len(module_content)):
                    lines = e.start[0] - module_content[mod_lvl][0] + 1
                    length = int(config['OPTIONAL']['MaxModuleLines'])
                    if lines > length:
                        print("Too many lines in module " + str(e.finish) + " " + module_content[mod_lvl][2])
                    mod_lvl -= 1
                    module_content.pop()
            if mod_lvl > -1 and tokens[i].token_type == "DEDENT" and tokens[i + 1].token_type != "DEDENT"\
                    and (tokens[i].start[1] == module_content[mod_lvl][1] or (module_content[mod_lvl][1] - tokens[i].start[1]) % indent == 0):
                r1 = count_dedents(tokens, i)
                e = find_last_module_element(tokens, i)
                for j in range(r1):
                    lines = e.start[0] - module_content[mod_lvl][0] + 1
                    length = int(config['OPTIONAL']['MaxModuleLines'])
                    if lines > length:
                        print("Too many lines in module " + str(e.finish) + " " + module_content[mod_lvl][2])
                    mod_lvl -= 1
                    module_content.pop()

            if tokens[i].content in modules and check_correct_module(tokens, i):
                mod_lvl += 1
                module_content.append([])
                module_content[mod_lvl].append(tokens[i].start[0])
                module_content[mod_lvl].append(tokens[i].start[1])
                module_content[mod_lvl].append(tokens[i].content)

        checked = False

        if config['NAMES']['CheckForbNames'] == 'yes':
            out = check_is_name_valid(tokens, i)
            if out != "":
                print(out)

        if config['NAMES']['FuncCase'] == 'snake':
            if is_func_decl(tokens, i):
                out = is_snake_case(tokens, i)
                if out:
                    print(out)

        if config['NAMES']['FuncCase'] == 'camel':
            if is_func_decl(tokens, i):
                out = is_camel_case(tokens, i)
                if out:
                    print(out)

        if config['NAMES']['VarNames'] == 'snake':
            if tokens[i].token_type == "NAME" and tokens[i + 1].content == "=":
                out = is_snake_case(tokens, i)
                if out:
                    print(out)

        if config['NAMES']['VarNames'] == 'camel':
            if tokens[i].token_type == "NAME" and tokens[i + 1].content == "=":
                out = is_camel_case(tokens, i)
                if out:
                    print(out)

        if config['NAMES']['ClassNames'] == 'ucamel':
            if is_class_decl(tokens, i):
                out = is_upper_camel(tokens, i)
                if out:
                    print(out)

        if config['SPACES']['SpacesBetwFuncsInClass'] != 'no':
            spaces = int(config['SPACES']['SpacesBetwFuncsInClass'])
            if not class_started and get_class_start(tokens, i) != (-1, -1):
                class_started = True
                class_start = get_class_start(tokens, i)
            elif class_started and is_end(tokens, i, class_start):
                class_started = False

            if class_started and tokens[i].content == 'def':
                out = check_func_spaces_1(tokens, i, spaces)
                if out:
                    print(out)

        if config['SPACES']['SpacesBetwFuncNotInClass'] != 'no':
            ext_spaces = int(config['SPACES']['SpacesBetwFuncNotInClass'])
            if not class_started and tokens[i].content == 'def':
                out = check_func_spaces_1(tokens, i, ext_spaces)
                if out:
                    print(out)

    if config['DEFAULT']['EndLine'] == 'yes':
        blank_line_in_the_end(tokens)


if __name__ == "__main__":
    main()
