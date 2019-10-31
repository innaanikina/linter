from errors import error_messages


def make_mes(line_number, element_number, error_number, file_name):
    return file_name + ':'\
           + str(line_number) + ':' \
           + str(element_number) + ': ' \
           + error_number + ' ' \
           + error_messages[error_number]
