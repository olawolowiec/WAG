from string_with_arrows import *

class Error:
    def __init__(self, begin, end, error_name, details):
        self.begin = begin
        self.end = end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'Plik {self.begin.fn}, wiersz {self.begin.ln + 1}'
        result += '\n\n' + string_with_arrows(self.begin.ftxt, self.begin, self.end)
        return result

class ExpectedCharError(Error):
	def __init__(self, begin, end, details):
		super().__init__(begin, end, 'Oczekiwany znak', details)
        
class IllegalCharError(Error):
    def __init__(self, begin, end, details):
        super().__init__(begin, end, 'Niedozwolony znak', details)


class InvalidSyntaxError(Error):
    def __init__(self, begin, end, details=''):
        super().__init__(begin, end, 'Niepoprawna składnia', details)


class RTError(Error):
    def __init__(self, begin, end, details, context):
        super().__init__(begin, end, 'Błąd czasu wykonywania', details)
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
            result = f'  Plik {pos.fn}, wiersz {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return 'Traceback (Najnowsze wywołane połączenie):\n' + result
