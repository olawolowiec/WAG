from error import *
from node import *
from tokens import *
from interpreter import *

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.progress_count = 0

    def register_progression(self):
        self.progress_count += 1

    def register(self, res):
        self.progress_count += res.progress_count
        if res.error: self.error = res.error
        return res.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
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
                "Expected '+', '-', '*', '/' or '^'"
            ))
        return res

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
                    "Expected ')'"
                ))

        return res.failure(InvalidSyntaxError
                           (tok.begin, tok.end,
                            "Expected int, float, '+', '-', '('"))

    def power(self):
        return self.bin_op(self.atom, (powerXD,), self.factor)

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

    def expr(self):
        res = ParseResult()

        if self.current_tok.matches(keywordXD, 'LICZBA'):
            res.register_progression()
            self.progress()
        if self.current_tok.matches(keywordXD, 'NAPIS'):
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

            if self.current_tok.type != equalXD:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.begin, self.current_tok.end,
                    "Expected '='"
                ))

            res.register_progression()
            self.progress()
            expr = res.register(self.expr())
            if res.error: return res
            return res.success(VarAssignNode(var_name, expr))

        node = res.register(self.bin_op(self.term, (plusXD, minusXD)))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.begin, self.current_tok.end,
                "Expected 'var', int, float, identifier, '+', '-' or '('"
            ))

        return res.success(node)

    ###################################

    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a
        res = ParseResult()
        left = res.register(func_a())
        if res.error: return res

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register_progression()
            self.progress()
            right = res.register(func_b())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)
