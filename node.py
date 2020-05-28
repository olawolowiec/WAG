class NumberNode:
	def __init__(self, tok):
		self.tok = tok

		self.begin = self.tok.begin
		self.end = self.tok.end

	def __repr__(self):
		return f'{self.tok}'

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
