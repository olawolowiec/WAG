from error import *
from interpreter import *

class Value:
  def __init__(self):
    self.set_pos()
    self.set_context()

  def set_pos(self, begin=None, end=None):
    self.begin = begin
    self.end = end
    return self

  def set_context(self, context=None):
    self.context = context
    return self

  def added_to(self, other):
    return None, self.illegal_operation(other)

  def subbed_by(self, other):
    return None, self.illegal_operation(other)

  def multed_by(self, other):
    return None, self.illegal_operation(other)

  def dived_by(self, other):
    return None, self.illegal_operation(other)

  def powed_by(self, other):
    return None, self.illegal_operation(other)

  def get_comparison_eq(self, other):
    return None, self.illegal_operation(other)

  def get_comparison_ne(self, other):
    return None, self.illegal_operation(other)

  def get_comparison_lt(self, other):
    return None, self.illegal_operation(other)

  def get_comparison_gt(self, other):
    return None, self.illegal_operation(other)

  def get_comparison_lte(self, other):
    return None, self.illegal_operation(other)

  def get_comparison_gte(self, other):
    return None, self.illegal_operation(other)

  def anded_by(self, other):
    return None, self.illegal_operation(other)

  def ored_by(self, other):
    return None, self.illegal_operation(other)

  def execute(self, args):
    return RTResult().failure(self.illegal_operation())

  def copy(self):
    raise Exception('Niezdefiniowana metoda copy')

  def is_true(self):
    return False

  def illegal_operation(self, other=None):
    if not other: other = self
    return RTError(
      self.begin, other.end,
      'Niedozwolona operacja',
      self.context
    )

class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, begin=None, end=None):
        self.begin = begin
        self.end = end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        if isinstance(other, Number):
            return (Number(self.value
                    + other.value).set_context(self.context), None)

    def subbed_by(self, other):
        if isinstance(other, Number):
            return (Number(self.value
                    - other.value).set_context(self.context), None)

    def multed_by(self, other):
        if isinstance(other, Number):
            return (Number(self.value
                    * other.value).set_context(self.context), None)

    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return (None, RTError(other.begin, other.end,
                        'Pamiętaj cholero nie dziel przez zero', self.context))

            return (Number(self.value
                    / other.value).set_context(self.context), None)

    def powed_by(self, other):
        if isinstance(other, Number):
            return (Number(self.value
                    ** other.value).set_context(self.context), None)

    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return (Number(int(self.value
                    == other.value)).set_context(self.context), None)

    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return (Number(int(self.value
                    != other.value)).set_context(self.context), None)

    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return (Number(int(self.value
                    < other.value)).set_context(self.context), None)

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return (Number(int(self.value
                    > other.value)).set_context(self.context), None)

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return (Number(int(self.value
                    <= other.value)).set_context(self.context), None)

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return (Number(int(self.value
                    >= other.value)).set_context(self.context), None)

    def anded_by(self, other):
        if isinstance(other, Number):
            return (Number(int(self.value
                    and other.value)).set_context(self.context), None)

    def ored_by(self, other):
        if isinstance(other, Number):
            return (Number(int(self.value
                    or other.value)).set_context(self.context), None)

    def notted(self):
        return (Number((1 if self.value
                == 0 else 0)).set_context(self.context), None)

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.begin, self.end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return self.value != 0

    def __repr__(self):
        return str(self.value)


class Number(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.begin, other.end,
                    'Pamiętaj cholero nie dziel przez zero',
                    self.context
                )

            return Number(self.value / other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def powed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def anded_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def ored_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.begin, self.end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return self.value != 0

    def __repr__(self):
        return str(self.value)

class List(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

    def added_to(self, other):
        new_list = self.copy()
        new_list.elements.append(other)
        return new_list, None

    def subbed_by(self, other):
        if isinstance(other, Number):
            new_list = self.copy()
            try:
                new_list.elements.pop(other.value)
                return new_list, None
            except :
                return None, RTError(
                    other.begin, other.end,
                    'Element o tym indeksie nie może zostać usunięty z listy, ponieważ jest spoza zakresu',
                    self.context
                )
        else:
                return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, List):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
            return new_list, None
        else:
            return None, Value.illegal_operation(self, other)

    def dived_by(self, other):
        if isinstance(other, Number):
            try:
                return self.elements[other.value], None
            except :
                return None, RTError(
                    other.begin, other.end,
                    'Element o tym indeksie nie może zostać pobrany z listy, ponieważ jest spoza zakresu',
                    self.context
                )
        else:
            return None, Value.illegar_operation(self, other)

    def copy(self):
        copy = List(self.elements[:])
        copy.set_pos(self.begin, self.end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return f'[{", ".join([str(x) for x in self.elements])}]'

class String(Value):
	def __init__(self, value):
		super().__init__()
		self.value = value

	def added_to(self, other):
		if isinstance(other, String):
			return String(self.value + other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def multed_by(self, other):
		if isinstance(other, Number):
			return String(self.value * other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def is_true(self):
		return len(self.value) > 0

	def copy(self):
		copy = String(self.value)
		copy.set_pos(self.begin, self.end)
		copy.set_context(self.context)
		return copy

	def __repr__(self):
		return f'"{self.value}"'
