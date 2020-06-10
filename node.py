
class NumberNode:
  def __init__(self, tok):
    self.tok = tok

    self.begin = self.tok.begin
    self.end = self.tok.end

  def __repr__(self):
    return f'{self.tok}'

class StringNode:
  def __init__(self, tok):
    self.tok = tok

    self.begin = self.tok.begin
    self.end = self.tok.end

  def __repr__(self):
    return f'{self.tok}'

class ListNode:
  def __init__(self, element_nodes, begin, end):
    self.element_nodes = element_nodes

    self.begin = begin
    self.end = end

class VarAccessNode:
  def __init__(self, var_name_tok):
    self.var_name_tok = var_name_tok

    self.begin = self.var_name_tok.begin
    self.end = self.var_name_tok.end

class VarAssignNode:
  def __init__(self, var_name_tok, value_node):
    self.var_name_tok = var_name_tok
    self.value_node = value_node

    self.begin = self.var_name_tok.begin
    self.end = self.value_node.end

class BinOpNode:
  def __init__(self, left_node, op_tok, right_node):
    self.left_node = left_node
    self.op_tok = op_tok
    self.right_node = right_node

    self.begin = self.left_node.begin
    self.end = self.right_node.end

  def __repr__(self):
    return f'({self.left_node}, {self.op_tok}, {self.right_node})'

class UnaryOpNode:
  def __init__(self, op_tok, node):
    self.op_tok = op_tok
    self.node = node

    self.begin = self.op_tok.begin
    self.end = node.end

  def __repr__(self):
    return f'({self.op_tok}, {self.node})'

class IfNode:
  def __init__(self, cases, else_case):
    self.cases = cases
    self.else_case = else_case

    self.begin = self.cases[0][0].begin
    self.end = (self.else_case or self.cases[len(self.cases) - 1])[0].end

class ForNode:
  def __init__(self, var_name_tok, start_value_node, end_value_node, step_value_node, body_node, should_return_null):
    self.var_name_tok = var_name_tok
    self.start_value_node = start_value_node
    self.end_value_node = end_value_node
    self.step_value_node = step_value_node
    self.body_node = body_node
    self.should_return_null = should_return_null

    self.begin = self.var_name_tok.begin
    self.end = self.body_node.end

class WhileNode:
  def __init__(self, condition_node, body_node, should_return_null):
    self.condition_node = condition_node
    self.body_node = body_node
    self.should_return_null = should_return_null

    self.begin = self.condition_node.begin
    self.end = self.body_node.end

class FuncDefNode:
  def __init__(self, var_name_tok, arg_name_toks, body_node, should_auto_return):
    self.var_name_tok = var_name_tok
    self.arg_name_toks = arg_name_toks
    self.body_node = body_node
    self.should_auto_return = should_auto_return

    if self.var_name_tok:
      self.begin = self.var_name_tok.begin
    elif len(self.arg_name_toks) > 0:
      self.begin = self.arg_name_toks[0].begin
    else:
      self.begin = self.body_node.begin

    self.end = self.body_node.end

class CallNode:
  def __init__(self, node_to_call, arg_nodes):
    self.node_to_call = node_to_call
    self.arg_nodes = arg_nodes

    self.begin = self.node_to_call.begin

    if len(self.arg_nodes) > 0:
      self.end = self.arg_nodes[len(self.arg_nodes) - 1].end
    else:
      self.end = self.node_to_call.end

class ReturnNode:
  def __init__(self, node_to_return, begin, end):
    self.node_to_return = node_to_return

    self.begin = begin
    self.end = end

class ContinueNode:
  def __init__(self, begin, end):
    self.begin = begin
    self.end = end

class BreakNode:
  def __init__(self, begin, end):
    self.begin = begin
    self.end = end