from string_with_arrows import *

class Error:
    def __init__(self, begin, end, error_name, details):
        self.begin = begin
        self.end = end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.begin.fn}, line {self.begin.ln + 1}'
        result += '\n\n' + string_with_arrows(self.begin.ftxt, self.begin, self.end)
        return result


class IllegalCharError(Error):
    def __init__(self, begin, end, details):
        super().__init__(begin, end, 'Illegal Character', details)


class InvalidSyntaxError(Error):
    def __init__(self, begin, end, details=''):
        super().__init__(begin, end, 'Invalid Syntax', details)


class RTError(Error):
    def __init__(self, begin, end, details, context):
        super().__init__(begin, end, 'Runtime Error', details)
        self.context = context

    def as_string(self):
        result = self.generate_traceback()
        result += f'{self.error_name}: {self.details}'
        result += '\n\n' + string_with_arrows(self.begin.ftxt, self.begin, self.end)
        return result

    def generate_traceback(self):
        result = ''
        pos = self.begin
        ctx = self.context

        while ctx:
            result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return 'Traceback (most recent call last):\n' + result
