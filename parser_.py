from error import *
from node import *
from tokens import *
from interpreter import *

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.last_registered_progress_count = 0
        self.progress_count = 0

    def register_progression(self):
        self.last_registered_progress_count = 1
        self.progress_count += 1

    def register(self, res):
        self.last_registered_progress_count = res.progress_count
        self.progress_count += res.progress_count
        if res.error: self.error = res.error
        return res.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.last_registered_progress_count == 0:
            self.error = error
        return self

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.progress()

    def progress(self, ):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok.type != eofXD:
            return res.failure(InvalidSyntaxError(
                self.current_tok.begin, self.current_tok.end,
                "Oczekiwany znak '+', '-', '*', '/' or '^'"
            ))
        return res


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
                        "Expected ')', 'LICZBA', 'JEŻELI', 'DOPÓKI', 'FUNKCJA', identifier, '+', '-', '(' or 'NIE'"
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
                    "Oczekiwano ')'"
                ))
        elif tok.type == lsquareXD:
            list_expr = res.register(self.list_expr())
            if res.error: return res
            return res.success(list_expr)

        elif tok.matches(keywordXD, 'JEŻELI'):
            if_expr = res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)
        elif tok.matches(keywordXD, 'DOPÓKI'):
            while_expr = res.register(self.while_expr())
            if res.error: return res
            return res.success(while_expr)

        elif tok.matches(keywordXD, 'FUNKCJA'):
            func_def = res.register(self.func_def())
            if res.error: return res
            return res.success(func_def)

        return res.failure(InvalidSyntaxError
                           (tok.begin, tok.end,
                            "Oczekiwano int, float, '+', '-', '(', 'JEŻELI', 'DOPÓKI', 'FUNKCJA'"))

    def power(self):
        return self.bin_op(self.call, (powerXD,), self.factor)

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (plusXD, minusXD):
            res.register(self.progress())
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))

        return self.power()

    def term(self):
        return self.bin_op(self.factor, (mulXD, divXD))
    
    def arith_expr(self):
        return self.bin_op(self.term, (plusXD, minusXD))
    
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
				"Oczekiwano int, float, identifier, '+', '-', '(' or 'NIE'"
			))

        return res.success(node)

    def expr(self):
        res = ParseResult()

        if self.current_tok.matches(keywordXD, 'ZMIENNA'):
            res.register_progression()
            self.progress()

            if self.current_tok.type != identifierXD:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.begin, self.current_tok.end,
                    "Oczekiwany identyfikator"
                ))

            var_name = self.current_tok
            res.register_progression()
            self.progress()

            if self.current_tok.type != equalXD:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.begin, self.current_tok.end,
                    "Oczekiwany znak '='"
                ))

            res.register_progression()
            self.progress()
            expr = res.register(self.expr())
            if res.error: return res
            return res.success(VarAssignNode(var_name, expr))

        node = res.register(self.bin_op(self.comp_expr, ((keywordXD, 'I'), (keywordXD, 'LUB'))))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.begin, self.current_tok.end,
                "Oczekiwano 'ZMIENNA', int, float, identifier, '+', '-' or '('"
            ))

        return res.success(node)


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

    def list_expr(self):
        res = ParseResult()
        element_nodes = []
        begin = self.current_tok.begin.copy()

        if self.current_tok.type != lsquareXD:
            return res.failure(InvalidSyntaxError(
                self.current_tok.begin, self.current_tok.end,
                f"Oczekiwany znak '['"
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
                    "Oczekiwany znak ']', 'ZMIENNA', 'IF', 'FOR', 'WHILE', 'FUN', int, float, identifier, '+', '-', '(', '[' or 'Nie'"
                ))

            while self.current_tok.type == commaXD:
                res.register_progression()
                self.progress()

                element_nodes.append(res.register(self.expr()))
                if res.error: return res

            if self.current_tok.type != rsquareXD:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.begin, self.current_tok.end,
                    f"Oczekiwany znak ',' lub ']'"
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
        cases = []
        else_case = None

        if not self.current_tok.matches(keywordXD, 'JEŻELI'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.begin, self.current_tok.end,
                f"Expected 'JEŻELI'"
            ))

        res.register_progression()
        self.progress()

        condition = res.register(self.expr())
        if res.error: return res

        if not self.current_tok.matches(keywordXD, 'TO'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.begin, self.current_tok.end,
                f"Expected 'TO'"
            ))

        res.register_progression()
        self.progress()

        expr = res.register(self.expr())
        if res.error: return res
        cases.append((condition, expr))

        while self.current_tok.matches(keywordXD, 'BĄDŹ'):
            res.register_progression()
            self.progress()

            condition = res.register(self.expr())
            if res.error: return res

            if not self.current_tok.matches(keywordXD, 'TO'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.begin, self.current_tok.end,
                    f"Expected 'TO'"
                ))

            res.register_progression()
            self.progress()

            expr = res.register(self.expr())
            if res.error: return res
            cases.append((condition, expr))

        if self.current_tok.matches(keywordXD, 'W_PRZECIWNYM_PRZYPADKU'):
            res.register_progression()
            self.progress()

            else_case = res.register(self.expr())
            if res.error: return res

        return res.success(IfNode(cases, else_case))

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

        body = res.register(self.expr())
        if res.error: return res

        return res.success(WhileNode(condition, body))

    def func_def(self):
        res = ParseResult()

        if not self.current_tok.matches(keywordXD, 'FUNKCJA'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.begin, self.current_tok.end,
                f"Expected 'FUNKCJA'"
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

        if self.current_tok.type != arrowXD:
            return res.failure(InvalidSyntaxError(
                self.current_tok.begin, self.current_tok.end,
                f"Expected '->'"
            ))

        res.register_progression()
        self.progress()
        node_to_return = res.register(self.expr())
        if res.error: return res

        return res.success(FuncDefNode(
            var_name_tok,
            arg_name_toks,
            node_to_return
        ))


