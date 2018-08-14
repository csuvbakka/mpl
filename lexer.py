import sys
import re
from enum import Enum

re.ASCII


class MplSyntaxError(Exception):
        pass


class Tokens(Enum):
    KEYWORD = 1
    SEPARATOR = 2
    LITERAL = 3
    IDENTIFIER = 4
    OPERATOR = 5
    INDENTATION = 6


keywords = ['int', 'float', 'double', 'array', 'bool', 'return', 'class']
separators = ['{', '}', '<', '>', ',']
operators = ['=']
literals = r'^([0-9]+|".*")$'
identifiers = r'^(\w+)$'


symbol_table = []

def process_word(word):
    if word in keywords:
        return (Tokens.KEYWORD, word)
    if word in separators:
        return (Tokens.SEPARATOR, word)
    if word in operators:
        return (Tokens.OPERATOR, word)

    m = re.match(literals, word)
    if m:
        return (Tokens.LITERAL, m.group(1))
    m = re.match(identifiers, word)
    if m:
        return (Tokens.IDENTIFIER, m.group(1))

    return None


def process_sub_word(word, index):
    valid_tokens = []
    subword = ''
    for i in range(index, len(word)):
        subword += word[i]
        token = process_word(subword)
        if token:
            valid_tokens.append((i, token))

    return valid_tokens


def process_leading_spaces(line, index):
    space_count = len(line) - len(line.lstrip())
    if space_count % 4 != 0:
        raise MplSyntaxError('Invalid space count {} on line {}:\n{}'
                             .format(space_count, index, line))
    indent_count = space_count / 4
    return indent_count


def process_line(line, line_index):
    if len(line.strip()) == 0:
        return

    indent_count = process_leading_spaces(line, line_index)
    if indent_count > 0:
        symbol_table.append((Tokens.INDENTATION, indent_count))
    words = line.split()
    for word in words:
        token = process_word(word)
        if token:
            symbol_table.append(token)
        else:
            index = 0
            while index < len(word):
                tokens = process_sub_word(word, index)
                if tokens:
                    index, token = tokens[-1]
                    index += 1
                    symbol_table.append(token)
                else:
                    break


if __name__ == '__main__':
    mpl_file = sys.argv[1]
    with open(mpl_file, 'r') as f:
        for line_index, line in enumerate(f.readlines()):
            process_line(line, line_index)

    for symbol in symbol_table:
        print(symbol)
