

intXD		= 'int'
floatXD    	= 'float'
stringXD	= 'string'
identifierXD= 'identifier'
keywordXD	= 'keyword'
plusXD     	= 'plus'
minusXD    	= 'minus'
mulXD      	= 'mul'
divXD      	= 'div'
powXD		= 'pow'
eqXD		= 'eq'
lparenXD   	= 'lparen'
rparenXD   	= 'rparen'
lsquareXD   = 'lsquare'
rsquareXD   = 'rsquare'
eeXD		= 'ee'
neXD		= 'ne'
ltXD		= 'lt'
gtXD		= 'gt'
lteXD		= 'lte'
gteXD		= 'gte'
commaXD		= 'comma'
arrowXD		= 'arrow'
newlineXD	= 'newline'
eofXD		= 'eof'
colonXD     = 'colon'

KEYWORDS = [
  'ZMIENNA',#VAR
  'ORAZ',#AND
  'LUB',#OR
  'NIE',#NOT
  'JEŻELI',#IF  
  'BĄDŹ',#ELIF
  'PRZECIWNIE',#ELSE
  #JEŻELI .. WYKONAJ .. BĄDŹ .. WYKONAJ ..  PRZECIWNIE ..
  'DLA',#FOR
  'DO',#(DLA).. DO .. (KROK) .. WYKONAJ; ...
  'KROK',#STEP
  'DOPÓKI',#WHILE
  'DOPÓTY',#(DOPÓKI)..DOPÓTY; ..
  'TEZA',#FUN
  #TEZA (); .. ; PODSUMOWUJĄC .. ; CO_KOŃCZY_DOWÓD
  'WYKONAJ',#THEN
  'CO_KOŃCZY_DOWÓD',#END
  'PODSUMOWUJĄC',#RETURN
  'KONTYNUUJ',#CONTINUE
  'PRZERWIJ',#BREAK
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