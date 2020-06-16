from wag import *
from tokens import *
from position import *
from error import *
import string
import string_with_arrows

digits = '0123456789'
letters = string.ascii_letters + 'ĄąĘęŻżŹźÓóŚś'
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
            elif self.current_char == '"':
                tokens.append(self.make_string())
            elif self.current_char == '+':
                tokens.append(Token(plusXD, begin=self.pos))
                self.progress()
            elif self.current_char == '-':
                tokens.append(self.make_minus_or_arrow())
            elif self.current_char == '*':
                tokens.append(Token(mulXD, begin=self.pos))
                self.progress()
            elif self.current_char == '^':
                tokens.append(Token(powerXD, begin=self.pos))
                self.progress()
            elif self.current_char == '/':
                tokens.append(Token(divXD, begin=self.pos))
                self.progress()
            elif self.current_char == '(':
                tokens.append(Token(lparenXD, begin=self.pos))
                self.progress()
            elif self.current_char == ')':
                tokens.append(Token(rparenXD, begin=self.pos))
                self.progress()
            elif self.current_char == '[':
                tokens.append(Token(lsquareXD, begin=self.pos))
                self.progress()
            elif self.current_char == ']':
                tokens.append(Token(rsquareXD, begin=self.pos))
                self.progress()
            elif self.current_char == '!':
                token, error = self.make_not_equals()
                if error: return [], error
                tokens.append(token)
            elif self.current_char == '=':
                tokens.append(self.make_equals())
            elif self.current_char == '<':
                tokens.append(self.make_less_than())
            elif self.current_char == '>':
                tokens.append(self.make_greater_than())
            elif self.current_char == ',':
                tokens.append(Token(commaXD, begin=self.pos))
                self.progress()
            else:
                begin = self.pos.copy()
                char = self.current_char
                self.progress()
                return [], IllegalCharError(begin, self.pos, "'" + char + "'")

        tokens.append(Token(eofXD, begin=self.pos))
        return tokens, None

    def make_minus_or_arrow(self):
        tok_type = minusXD
        begin = self.pos.copy()
        self.progress()

        if self.current_char == '>':
            self.progress()
            tok_type = arrowXD

        return Token(tok_type, begin=begin, end=self.pos)

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

    def make_string(self):
        string = ''
        begin = self.pos.copy()
        escape_character = False
        self.progress()

        escape_characters = {
            'n': '\n',
            't': '\t'
        }

        while self.current_char != None and (self.current_char != '"' or escape_character):
            if escape_character:
                string += escape_characters.get(self.current_char, self.current_char)
            else:
                if self.current_char == '\\':
                    escape_character = True
                else:
                    string += self.current_char
            self.progress()
            escape_character = False

        self.progress()
        return Token(stringXD, string, begin, self.pos)

    def make_not_equals(self):
        begin = self.pos.copy()
        self.progress()

        if self.current_char == '=':
            self.progress()
            return Token(neXD, begin = begin, end = self.pos), None

        self.progress()
        return None, ExpectedCharError(begin, self.pos, "'=' (after '!')")
    
    def make_equals(self):
        tok_type = equalXD
        begin = self.pos.copy()
        self.progress()

        if self.current_char == '=':
            self.progress()
            tok_type = eeXD

        return Token(tok_type, begin = begin, end = self.pos)

    def make_less_than(self):
        tok_type = ltXD
        begin = self.pos.copy()
        self.progress()

        if self.current_char == '=':
            self.progress()
            tok_type = lteXD

        return Token(tok_type, begin = begin, end = self.pos)

    def make_greater_than(self):
        tok_type = gtXD
        begin = self.pos.copy()
        self.progress()

        if self.current_char == '=':
            self.progress()
            tok_type = gteXD

        return Token(tok_type, begin = begin, end = self.pos)