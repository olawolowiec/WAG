from tokens import *
from values import *

class RTResult:
	def __init__(self):
		self.value = None
		self.error = None

	def register(self, res):
		if res.error: self.error = res.error
		return res.value

	def success(self, value):
		self.value = value
		return self

	def failure(self, error):
		self.error = error
		return self

class Context:
	def __init__(self, display_name, parent=None, parent_entry_pos=None):
		self.display_name = display_name
		self.parent = parent
		self.parent_entry_pos = parent_entry_pos
		self.symbol_table = None

class SymbolTable:
	def __init__(self, parent=None):
		self.symbols = {}
		self.parent = parent

	def get(self, name):
		value = self.symbols.get(name, None)
		if value == None and self.parent:
			return self.parent.get(name)
		return value

	def set(self, name, value):
		self.symbols[name] = value

	def remove(self, name):
		del self.symbols[name]

class Interpreter:
	def visit(self, node, context):
		method_name = f'visit_{type(node).__name__}'
		method = getattr(self, method_name, self.no_visit_method)
		return method(node, context)

	def no_visit_method(self, node, context):
		raise Exception(f'No visit_{type(node).__name__} zdefiniowana metoda')


	def visit_NumberNode(self, node, context):
		return RTResult().success(
			Number(node.tok.value).set_context(context).set_pos(node.begin, node.end)
		)

	def visit_ListNode(self, node, context):
		res = RTResult()
		elements = []

		for element_node in node.element_nodes:
			elements.append(res.register(self.visit(element_node, context)))
			if res.error: return res

		return res.success(
			List(elements).set_context(context).set_pos(node.begin, node.end)
			)

	def visit_VarAccessNode(self, node, context):
		res = RTResult()
		var_name = node.var_name_tok.value
		value = context.symbol_table.get(var_name)

		if not value:
			return res.failure(RTError(
				node.begin, node.end,
				f"'{var_name}' nie została zdefiniowana",
				context
			))

		value = value.copy().set_pos(node.begin, node.end)
		return res.success(value)

	def visit_VarAssignNode(self, node, context):
		res = RTResult()
		var_name = node.var_name_tok.value
		value = res.register(self.visit(node.value_node, context))
		if res.error: return res

		context.symbol_table.set(var_name, value)
		return res.success(value)

	def visit_BinOpNode(self, node, context):
		res = RTResult()
		left = res.register(self.visit(node.left_node, context))
		if res.error: return res
		right = res.register(self.visit(node.right_node, context))
		if res.error: return res

		if node.op_tok.type == plusXD:
			result, error = left.added_to(right)
		elif node.op_tok.type == minusXD:
			result, error = left.subbed_by(right)
		elif node.op_tok.type == mulXD:
			result, error = left.multed_by(right)
		elif node.op_tok.type == divXD:
			result, error = left.dived_by(right)
		elif node.op_tok.type == powerXD:
			result, error = left.powed_by(right)
		elif node.op_tok.type == eeXD:
			result, error = left.get_comparison_eq(right)
		elif node.op_tok.type == neXD:
			result, error = left.get_comparison_ne(right)
		elif node.op_tok.type == ltXD:
			result, error = left.get_comparison_lt(right)
		elif node.op_tok.type == gtXD:
			result, error = left.get_comparison_gt(right)
		elif node.op_tok.type == lteXD:
			result, error = left.get_comparison_lte(right)
		elif node.op_tok.type == gteXD:
			result, error = left.get_comparison_gte(right)
		elif node.op_tok.matches(keywordXD, 'I'):
			result, error = left.anded_by(right)
		elif node.op_tok.matches(keywordXD, 'LUB'):
			result, error = left.ored_by(right)

		if error:
			return res.failure(error)
		else:
			return res.success(result.set_pos(node.begin, node.end))
        
	def visit_UnaryOpNode(self, node, context):
		res = RTResult()
		number = res.register(self.visit(node.node, context))
		if res.error: return res

		error = None

		if node.op_tok.type == minusXD:
			number, error = number.multed_by(Number(-1))
		elif node.op_tok.matches(keywordXD, 'NIE'):
			number, error = number.notted()
            
		if error:
			return res.failure(error)
		else:
			return res.success(number.set_pos(node.begin, node.end))

	def visit_IfNode(self, node, context):
		res = RTResult()

		for condition, expr in node.cases:
			condition_value = res.register(self.visit(condition, context))
			if res.error: return res

			if condition_value.is_true():
				expr_value = res.register(self.visit(expr, context))
				if res.error: return res
				return res.success(expr_value)

		if node.else_case:
			else_value = res.register(self.visit(node.else_case, context))
			if res.error: return res
			return res.success(else_value)

		return res.success(None)

	def visit_WhileNode(self, node, context):
		res = RTResult()
		elements = []

		while True:
			condition = res.register(self.visit(node.condition_node, context))
			if res.error: return res

			if not condition.is_true(): break

			elements.append(res.register(self.visit(node.body_node, context)))
			if res.error: return res

		return res.success(
			List(elements).set_context(context).set_pos(node.begin, node.end)
		)