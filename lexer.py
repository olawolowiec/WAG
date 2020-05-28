from wag import *
from tokens import *
from position import *
import string
import string_with_arrows

digits = '0123456789'
letters = string.ascii_letters
letters_digits = letters + digits

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.progress()

    def progress(self):
        self.pos.progress(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.progress()
            elif self.current_char in digits:
                tokens.append(self.make_number())
            elif self.current_char in letters:
                tokens.append(self.make_identifier())
            elif self.current_char == '+':
                tokens.append(Token(plusXD, begin=self.pos))
                self.progress()
            elif self.current_char == '-':
                tokens.append(Token(minusXD, begin=self.pos))
                self.progress()
            elif self.current_char == '*':
                tokens.append(Token(mulXD, begin=self.pos))
                self.progress()
            elif self.current_char == '^':
                tokens.append(Token(powerXD, begin=self.pos))
                self.progress()
            elif self.current_char == '/':
                tokens.append(Token(divXD, begin=self.pos))
                self.progress()
            elif self.current_char == '=':
                tokens.append(Token(equalXD, begin=self.pos))
                self.progress()
            elif self.current_char == '(':
                tokens.append(Token(lparenXD, begin=self.pos))
                self.progress()
            elif self.current_char == ')':
                tokens.append(Token(rparenXD, begin=self.pos))
                self.progress()
            else:
                begin = self.pos.copy()
                char = self.current_char
                self.progress()
                return [], IllegalCharError(begin, self.pos, "'" + char + "'")

        tokens.append(Token(eofXD, begin=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        begin = self.pos.copy()

        while self.current_char != None and self.current_char in digits + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
            num_str += self.current_char
            self.progress()

        if dot_count == 0:
            return Token(intXD, int(num_str), begin, self.pos)
        else:
            return Token(floatXD, float(num_str), begin, self.pos)


    def make_identifier(self):
        id_str = ''
        begin = self.pos.copy()

        while self.current_char != None and self.current_char in letters_digits + '_':
            id_str += self.current_char
            self.progress()

        tok_type = keywordXD if id_str in keywordsXD else identifierXD
        return Token(tok_type, id_str, begin, self.pos)