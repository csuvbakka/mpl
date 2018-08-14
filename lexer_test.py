import unittest
from lexer import Tokens, process_line
import lexer


class LexerTest(unittest.TestCase):
    def test_assignment(self):
        process_line('foo = int{42}', 0)
        self.assertEqual(lexer.symbol_table,
                         [(Tokens.IDENTIFIER, 'foo'), (Tokens.OPERATOR, '='), 
                          (Tokens.KEYWORD, 'int'),  (Tokens.SEPARATOR, '{'),
                          (Tokens.LITERAL, '42'),  (Tokens.SEPARATOR, '}')])

    def test_templated_type(self):
        lexer.symbol_table = []
        process_line('s = array<Foo>{1, "banan"}', 0)
        self.assertEqual(lexer.symbol_table,
                         [(Tokens.IDENTIFIER, 's'), (Tokens.OPERATOR, '='), (Tokens.KEYWORD, 'array'),
                          (Tokens.SEPARATOR, '<'), (Tokens.IDENTIFIER, 'Foo'), (Tokens.SEPARATOR, '>'),
                          (Tokens.SEPARATOR, '{'), (Tokens.LITERAL, '1'), (Tokens.SEPARATOR, ','),
                          (Tokens.LITERAL, '"banan"'), (Tokens.SEPARATOR, '}')])


if __name__ == '__main__':
    unittest.main()
