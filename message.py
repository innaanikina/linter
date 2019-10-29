from errors import error_messages


def make_message(line_number, element_number, error_number):
    return 'Line ' + line_number + ', ' \
           + element_number + ': ' + error_messages[error_number]


def make_message_line(line_number, error_number):
    return 'Line ' + line_number + ': ' + error_messages[error_number]


def make_full_message(line_number, element_number, error_number):
    return 'Line ' + str(line_number) + ': ' + str(element_number) \
           + ' ' + error_number + ' ' + error_messages[error_number]


def make_message_file(line_number, element_number, error_number, file_name):
    return file_name + ':'\
           + str(line_number) + ':' \
           + str(element_number) + ': ' \
           + error_number + ' ' \
           + error_messages[error_number]
