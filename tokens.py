intXD = 'integer'
floatXD = 'float'
stringXD = 'string'
identifierXD = 'identifier'
keywordXD = 'keyword'
plusXD = 'plus'
minusXD = 'minus'
mulXD = 'mul'
divXD = 'div'
powerXD = 'power'
lparenXD = 'lparen'
rparenXD = 'rparen'
lsquareXD = 'lsquare'
rsquareXD = 'rsquare'
equalXD ='equal'
eofXD = 'eof'
eeXD = 'ee' 
neXD = 'ne' 
ltXD = 'lt' 
gtXD = 'gt' 
lteXD = 'lte' 
gteXD = 'gte'
commaXD = 'comma'
arrowXD = 'arrow'



keywordsXD = [
    'LICZBA',
    'TABLICA',
    'WARTOŚĆ_LOGICZNA',
    'LUB',
    'I',
    'NIE',
    'DOPÓKI',
    'DOPÓTY',
    'JEŻELI', #if
    'BĄDŹ', #else if
    'W_PRZECIWNYM_PRZYPADKU', #else
    "TO",  #then
    'FUNKCJA'
]

class Token:
    def __init__(self, type_, value=None, begin=None, end=None):
        self.type = type_
        self.value = value

        if begin:
            self.begin = begin.copy()
            self.end = begin.copy()
            self.end.progress()

        if end:
            self.end = end.copy()

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'