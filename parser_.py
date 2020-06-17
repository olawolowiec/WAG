
from error import *
from node import *
from tokens import *
from interpreter import *

# PARSE RESULT

class ParseResult:
  def __init__(self):
    self.error = None
    self.node = None
    self.last_registered_progression_count = 0
    self.progression_count = 0
    self.to_reverse_count = 0

  def register_progression(self):
    self.last_registered_progression_count = 1
    self.progression_count += 1

  def register(self, res):
    self.last_registered_progression_count = res.progression_count
    self.progression_count += res.progression_count
    if res.error: self.error = res.error
    return res.node

  def try_register(self, res):
    if res.error:
      self.to_reverse_count = res.progression_count
      return None
    return self.register(res)

  def success(self, node):
    self.node = node
    return self

  def failure(self, error):
    if not self.error or self.last_registered_progression_count == 0:
      self.error = error
    return self

# PARSER

class Parser:
  def __init__(self, tokens):
    self.tokens = tokens
    self.tok_idx = -1
    self.progress()

  def progress(self):
    self.tok_idx += 1
    self.update_current_tok()
    return self.current_tok

  def reverse(self, amount=1):
    self.tok_idx -= amount
    self.update_current_tok()
    return self.current_tok

  def update_current_tok(self):
    if self.tok_idx >= 0 and self.tok_idx < len(self.tokens):
      self.current_tok = self.tokens[self.tok_idx]

  def parse(self):
    res = self.statements()
    if not res.error and self.current_tok.type != eofXD:
      return res.failure(InvalidSyntaxError(
        self.current_tok.begin, self.current_tok.end,
        "Token cannot appear after previous tokens"
      ))
    return res

  ###################################

  def statements(self):
    res = ParseResult()
    statements = []
    begin = self.current_tok.begin.copy()

    while self.current_tok.type == newlineXD:
      res.register_progression()
      self.progress()

    statement = res.register(self.statement())
    if res.error: return res
    statements.append(statement)

    more_statements = True

    while True:
      newline_count = 0
      while self.current_tok.type == newlineXD:
        res.register_progression()
        self.progress()
        newline_count += 1
      if newline_count == 0:
        more_statements = False
      
      if not more_statements: break
      statement = res.try_register(self.statement())
      if not statement:
        self.reverse(res.to_reverse_count)
        more_statements = False
        continue
      statements.append(statement)

    return res.success(ListNode(
      statements,
      begin,
      self.current_tok.end.copy()
    ))

  def statement(self):
    res = ParseResult()
    begin = self.current_tok.begin.copy()

    if self.current_tok.matches(keywordXD, 'PODSUMOWUJĄC'):
      res.register_progression()
      self.progress()

      expr = res.try_register(self.expr())
      if not expr:
        self.reverse(res.to_reverse_count)
      return res.success(ReturnNode(expr, begin, self.current_tok.begin.copy()))
    
    if self.current_tok.matches(keywordXD, 'KONTYNUUJ'):
      res.register_progression()
      self.progress()
      return res.success(ContinueNode(begin, self.current_tok.begin.copy()))
      
    if self.current_tok.matches(keywordXD, 'BREAK'):
      res.register_progression()
      self.progress()
      return res.success(BreakNode(begin, self.current_tok.begin.copy()))

    expr = res.register(self.expr())
    if res.error:
      return res.failure(InvalidSyntaxError(
        self.current_tok.begin, self.current_tok.end,
        "Expected 'PODSUMOWUJĄC', 'KONTYNUUJ', 'BREAK', 'ZMIENNA', 'JEŻELI', 'FOR', 'DOPÓKI', 'TEZA', int, float, identifier, '+', '-', '(', '[' or 'NIE'"
      ))
    return res.success(expr)

  def expr(self):
    res = ParseResult()

    if self.current_tok.matches(keywordXD, 'ZMIENNA'):
      res.register_progression()
      self.progress()

      if self.current_tok.type != identifierXD:
        return res.failure(InvalidSyntaxError(
          self.current_tok.begin, self.current_tok.end,
          "Expected identifier"
        ))

      var_name = self.current_tok
      res.register_progression()
      self.progress()

      if self.current_tok.type != eqXD:
        return res.failure(InvalidSyntaxError(
          self.current_tok.begin, self.current_tok.end,
          "Expected '='"
        ))

      res.register_progression()
      self.progress()
      expr = res.register(self.expr())
      if res.error: return res
      return res.success(VarAssignNode(var_name, expr))

    node = res.register(self.bin_op(self.comp_expr, ((keywordXD, 'ORAZ'), (keywordXD, 'LUB'))))

    if res.error:
      return res.failure(InvalidSyntaxError(
        self.current_tok.begin, self.current_tok.end,
        "Expected 'ZMIENNA', 'JEŻELI', 'FOR', 'DOPÓKI', 'TEZA', int, float, identifier, '+', '-', '(', '[' or 'NIE'"
      ))

    return res.success(node)

  def comp_expr(self):
    res = ParseResult()

    if self.current_tok.matches(keywordXD, 'NIE'):
      op_tok = self.current_tok
      res.register_progression()
      self.progress()

      node = res.register(self.comp_expr())
      if res.error: return res
      return res.success(UnaryOpNode(op_tok, node))
    
    node = res.register(self.bin_op(self.arith_expr, (eeXD, neXD, ltXD, gtXD, lteXD, gteXD)))
    
    if res.error:
      return res.failure(InvalidSyntaxError(
        self.current_tok.begin, self.current_tok.end,
        "Expected int, float, identifier, '+', '-', '(', '[', 'JEŻELI', 'FOR', 'DOPÓKI', 'TEZA' or 'NIE'"
      ))

    return res.success(node)

  def arith_expr(self):
    return self.bin_op(self.term, (plusXD, minusXD))

  def term(self):
    return self.bin_op(self.factor, (mulXD, divXD))

  def factor(self):
    res = ParseResult()
    tok = self.current_tok

    if tok.type in (plusXD, minusXD):
      res.register_progression()
      self.progress()
      factor = res.register(self.factor())
      if res.error: return res
      return res.success(UnaryOpNode(tok, factor))

    return self.power()

  def power(self):
    return self.bin_op(self.call, (powXD, ), self.factor)

  def call(self):
    res = ParseResult()
    atom = res.register(self.atom())
    if res.error: return res

    if self.current_tok.type == lparenXD:
      res.register_progression()
      self.progress()
      arg_nodes = []

      if self.current_tok.type == rparenXD:
        res.register_progression()
        self.progress()
      else:
        arg_nodes.append(res.register(self.expr()))
        if res.error:
          return res.failure(InvalidSyntaxError(
            self.current_tok.begin, self.current_tok.end,
            "Expected ')', 'ZMIENNA', 'JEŻELI', 'FOR', 'DOPÓKI', 'TEZA', int, float, identifier, '+', '-', '(', '[' or 'NIE'"
          ))

        while self.current_tok.type == commaXD:
          res.register_progression()
          self.progress()

          arg_nodes.append(res.register(self.expr()))
          if res.error: return res

        if self.current_tok.type != rparenXD:
          return res.failure(InvalidSyntaxError(
            self.current_tok.begin, self.current_tok.end,
            f"Expected ',' or ')'"
          ))

        res.register_progression()
        self.progress()
      return res.success(CallNode(atom, arg_nodes))
    return res.success(atom)

  def atom(self):
    res = ParseResult()
    tok = self.current_tok

    if tok.type in (intXD, floatXD):
      res.register_progression()
      self.progress()
      return res.success(NumberNode(tok))

    elif tok.type == stringXD:
      res.register_progression()
      self.progress()
      return res.success(StringNode(tok))

    elif tok.type == identifierXD:
      res.register_progression()
      self.progress()
      return res.success(VarAccessNode(tok))

    elif tok.type == lparenXD:
      res.register_progression()
      self.progress()
      expr = res.register(self.expr())
      if res.error: return res
      if self.current_tok.type == rparenXD:
        res.register_progression()
        self.progress()
        return res.success(expr)
      else:
        return res.failure(InvalidSyntaxError(
          self.current_tok.begin, self.current_tok.end,
          "Expected ')'"
        ))

    elif tok.type == lsquareXD:
      list_expr = res.register(self.list_expr())
      if res.error: return res
      return res.success(list_expr)
    
    elif tok.matches(keywordXD, 'JEŻELI'):
      if_expr = res.register(self.if_expr())
      if res.error: return res
      return res.success(if_expr)

    elif tok.matches(keywordXD, 'FOR'):
      for_expr = res.register(self.for_expr())
      if res.error: return res
      return res.success(for_expr)
#MOŻE DODAĆ TEŻ Z THEN
    elif tok.matches(keywordXD, 'DOPÓKI'):
      while_expr = res.register(self.while_expr())
      if res.error: return res
      return res.success(while_expr)

    elif tok.matches(keywordXD, 'TEZA'):
      func_def = res.register(self.func_def())
      if res.error: return res
      return res.success(func_def)

    return res.failure(InvalidSyntaxError(
      tok.begin, tok.end,
      "Expected int, float, identifier, '+', '-', '(', '[', IF', 'FOR', 'DOPÓKI', 'TEZA'"
    ))

  def list_expr(self):
    res = ParseResult()
    element_nodes = []
    begin = self.current_tok.begin.copy()

    if self.current_tok.type != lsquareXD:
      return res.failure(InvalidSyntaxError(
        self.current_tok.begin, self.current_tok.end,
        f"Expected '['"
      ))

    res.register_progression()
    self.progress()

    if self.current_tok.type == rsquareXD:
      res.register_progression()
      self.progress()
    else:
      element_nodes.append(res.register(self.expr()))
      if res.error:
        return res.failure(InvalidSyntaxError(
          self.current_tok.begin, self.current_tok.end,
          "Expected ']', 'ZMIENNA', 'JEŻELI', 'FOR', 'DOPÓKI', 'TEZA', int, float, identifier, '+', '-', '(', '[' or 'NIE'"
        ))

      while self.current_tok.type == commaXD:
        res.register_progression()
        self.progress()

        element_nodes.append(res.register(self.expr()))
        if res.error: return res

      if self.current_tok.type != rsquareXD:
        return res.failure(InvalidSyntaxError(
          self.current_tok.begin, self.current_tok.end,
          f"Expected ',' or ']'"
        ))

      res.register_progression()
      self.progress()

    return res.success(ListNode(
      element_nodes,
      begin,
      self.current_tok.end.copy()
    ))

  def if_expr(self):
    res = ParseResult()
    all_cases = res.register(self.if_expr_cases('JEŻELI'))
    if res.error: return res
    cases, else_case = all_cases
    return res.success(IfNode(cases, else_case))

  def if_expr_b(self):
    return self.if_expr_cases('BĄDŹ')
    
  def if_expr_c(self):
    res = ParseResult()
    else_case = None

    if self.current_tok.matches(keywordXD, 'PRZECIWNIE'):
      res.register_progression()
      self.progress()

      if self.current_tok.type == newlineXD:
        res.register_progression()
        self.progress()

        statements = res.register(self.statements())
        if res.error: return res
        else_case = (statements, True)

        if self.current_tok.matches(keywordXD, 'CO_KOŃCZY_DOWÓD'):
          res.register_progression()
          self.progress()
        else:
          return res.failure(InvalidSyntaxError(
            self.current_tok.begin, self.current_tok.end,
            "Expected 'CO_KOŃCZY_DOWÓD'"
          ))
      else:
        expr = res.register(self.statement())
        if res.error: return res
        else_case = (expr, False)

    return res.success(else_case)

  def if_expr_b_or_c(self):
    res = ParseResult()
    cases, else_case = [], None

    if self.current_tok.matches(keywordXD, 'BĄDŹ'):
      all_cases = res.register(self.if_expr_b())
      if res.error: return res
      cases, else_case = all_cases
    else:
      else_case = res.register(self.if_expr_c())
      if res.error: return res
    
    return res.success((cases, else_case))

  def if_expr_cases(self, case_keyword):
    res = ParseResult()
    cases = []
    else_case = None

    if not self.current_tok.matches(keywordXD, case_keyword):
      return res.failure(InvalidSyntaxError(
        self.current_tok.begin, self.current_tok.end,
        f"Expected '{case_keyword}'"
      ))

    res.register_progression()
    self.progress()

    condition = res.register(self.expr())
    if res.error: return res

    if not self.current_tok.matches(keywordXD, 'WTEDY'):
      return res.failure(InvalidSyntaxError(
        self.current_tok.begin, self.current_tok.end,
        f"Expected 'WTEDY'"
      ))

    res.register_progression()
    self.progress()

    if self.current_tok.type == newlineXD:
      res.register_progression()
      self.progress()

      statements = res.register(self.statements())
      if res.error: return res
      cases.append((condition, statements, True))

      if self.current_tok.matches(keywordXD, 'CO_KOŃCZY_DOWÓD'):
        res.register_progression()
        self.progress()
      else:
        all_cases = res.register(self.if_expr_b_or_c())
        if res.error: return res
        new_cases, else_case = all_cases
        cases.extend(new_cases)
    else:
      expr = res.register(self.statement())
      if res.error: return res
      cases.append((condition, expr, False))

      all_cases = res.register(self.if_expr_b_or_c())
      if res.error: return res
      new_cases, else_case = all_cases
      cases.extend(new_cases)

    return res.success((cases, else_case))

  def for_expr(self):
    res = ParseResult()

    if not self.current_tok.matches(keywordXD, 'FOR'):
      return res.failure(InvalidSyntaxError(
        self.current_tok.begin, self.current_tok.end,
        f"Expected 'FOR'"
      ))

    res.register_progression()
    self.progress()

    if self.current_tok.type != identifierXD:
      return res.failure(InvalidSyntaxError(
        self.current_tok.begin, self.current_tok.end,
        f"Expected identifier"
      ))

    var_name = self.current_tok
    res.register_progression()
    self.progress()

    if self.current_tok.type != eqXD:
      return res.failure(InvalidSyntaxError(
        self.current_tok.begin, self.current_tok.end,
        f"Expected '='"
      ))
    
    res.register_progression()
    self.progress()

    start_value = res.register(self.expr())
    if res.error: return res

    if not self.current_tok.matches(keywordXD, 'TO'):
      return res.failure(InvalidSyntaxError(
        self.current_tok.begin, self.current_tok.end,
        f"Expected 'TO'"
      ))
    
    res.register_progression()
    self.progress()

    end_value = res.register(self.expr())
    if res.error: return res

    if self.current_tok.matches(keywordXD, 'STEP'):
      res.register_progression()
      self.progress()

      step_value = res.register(self.expr())
      if res.error: return res
    else:
      step_value = None

    if not self.current_tok.matches(keywordXD, 'WTEDY'):
      return res.failure(InvalidSyntaxError(
        self.current_tok.begin, self.current_tok.end,
        f"Expected 'WTEDY'"
      ))

    res.register_progression()
    self.progress()

    if self.current_tok.type == newlineXD:
      res.register_progression()
      self.progress()

      body = res.register(self.statements())
      if res.error: return res

      if not self.current_tok.matches(keywordXD, 'CO_KOŃCZY_DOWÓD'):
        return res.failure(InvalidSyntaxError(
          self.current_tok.begin, self.current_tok.end,
          f"Expected 'CO_KOŃCZY_DOWÓD'"
        ))

      res.register_progression()
      self.progress()

      return res.success(ForNode(var_name, start_value, end_value, step_value, body, True))
    
    body = res.register(self.statement())
    if res.error: return res

    return res.success(ForNode(var_name, start_value, end_value, step_value, body, False))

  def while_expr(self):
    res = ParseResult()

    if not self.current_tok.matches(keywordXD, 'DOPÓKI'):
      return res.failure(InvalidSyntaxError(
        self.current_tok.begin, self.current_tok.end,
        f"Expected 'DOPÓKI'"
      ))

    res.register_progression()
    self.progress()

    condition = res.register(self.expr())
    if res.error: return res

    if not self.current_tok.matches(keywordXD, 'DOPÓTY'):
      return res.failure(InvalidSyntaxError(
        self.current_tok.begin, self.current_tok.end,
        f"Expected 'DOPÓTY'"
      ))

    res.register_progression()
    self.progress()

    if self.current_tok.type == newlineXD:
      res.register_progression()
      self.progress()

      body = res.register(self.statements())
      if res.error: return res

      if not self.current_tok.matches(keywordXD, 'CO_KOŃCZY_DOWÓD'):
        return res.failure(InvalidSyntaxError(
          self.current_tok.begin, self.current_tok.end,
          f"Expected 'CO_KOŃCZY_DOWÓD'"
        ))

      res.register_progression()
      self.progress()

      return res.success(WhileNode(condition, body, True))
    
    body = res.register(self.statement())
    if res.error: return res

    return res.success(WhileNode(condition, body, False))

  def func_def(self):
    res = ParseResult()

    if not self.current_tok.matches(keywordXD, 'TEZA'):
      return res.failure(InvalidSyntaxError(
        self.current_tok.begin, self.current_tok.end,
        f"Expected 'TEZA'"
      ))

    res.register_progression()
    self.progress()

    if self.current_tok.type == identifierXD:
      var_name_tok = self.current_tok
      res.register_progression()
      self.progress()
      if self.current_tok.type != lparenXD:
        return res.failure(InvalidSyntaxError(
          self.current_tok.begin, self.current_tok.end,
          f"Expected '('"
        ))
    else:
      var_name_tok = None
      if self.current_tok.type != lparenXD:
        return res.failure(InvalidSyntaxError(
          self.current_tok.begin, self.current_tok.end,
          f"Expected identifier or '('"
        ))
    
    res.register_progression()
    self.progress()
    arg_name_toks = []

    if self.current_tok.type == identifierXD:
      arg_name_toks.append(self.current_tok)
      res.register_progression()
      self.progress()
      
      while self.current_tok.type == commaXD:
        res.register_progression()
        self.progress()

        if self.current_tok.type != identifierXD:
          return res.failure(InvalidSyntaxError(
            self.current_tok.begin, self.current_tok.end,
            f"Expected identifier"
          ))

        arg_name_toks.append(self.current_tok)
        res.register_progression()
        self.progress()
      
      if self.current_tok.type != rparenXD:
        return res.failure(InvalidSyntaxError(
          self.current_tok.begin, self.current_tok.end,
          f"Expected ',' or ')'"
        ))
    else:
      if self.current_tok.type != rparenXD:
        return res.failure(InvalidSyntaxError(
          self.current_tok.begin, self.current_tok.end,
          f"Expected identifier or ')'"
        ))

    res.register_progression()
    self.progress()

    if self.current_tok.type == arrowXD:
      res.register_progression()
      self.progress()

      body = res.register(self.expr())
      if res.error: return res

      return res.success(FuncDefNode(
        var_name_tok,
        arg_name_toks,
        body,
        True
      ))
    
    if self.current_tok.type != newlineXD:
      return res.failure(InvalidSyntaxError(
        self.current_tok.begin, self.current_tok.end,
        f"Expected '->' or NEWLINE"
      ))

    res.register_progression()
    self.progress()

    body = res.register(self.statements())
    if res.error: return res

    if not self.current_tok.matches(keywordXD, 'CO_KOŃCZY_DOWÓD'):
      return res.failure(InvalidSyntaxError(
        self.current_tok.begin, self.current_tok.end,
        f"Expected 'CO_KOŃCZY_DOWÓD'"
      ))

    res.register_progression()
    self.progress()
    
    return res.success(FuncDefNode(
      var_name_tok,
      arg_name_toks,
      body,
      False
    ))

  ###################################

  def bin_op(self, func_a, ops, func_b=None):
    if func_b == None:
      func_b = func_a
    
    res = ParseResult()
    left = res.register(func_a())
    if res.error: return res

    while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
      op_tok = self.current_tok
      res.register_progression()
      self.progress()
      right = res.register(func_b())
      if res.error: return res
      left = BinOpNode(left, op_tok, right)

    return res.success(left)