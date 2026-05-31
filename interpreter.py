from gramatica.KryptoParserVisitor import KryptoParserVisitor
from gramatica.KryptoParser import KryptoParser

from librerias import KRYPTOMATH
from librerias import KRYPTOMATRIX
from librerias import KRYPTOML
from librerias import KRYPTODL
from librerias.KRYPTOarchivos import read_file, write_file
from librerias.KRYPTOGRAF import get_chart
from librerias import KRYPTODS


class _ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value

class KryptoInterpreter(KryptoParserVisitor):

    def __init__(self):
        self._globals = {}        
        self._functions = {}      
        self._scope_stack = [{}]  

        self._BUILTINS = {}
        
        self._BUILTINS.update(KRYPTOMATH.FUNCTIONS)
        self._BUILTINS.update(KRYPTOMATRIX.FUNCTIONS)
        self._BUILTINS.update(KRYPTOML.FUNCTIONS)
        self._BUILTINS.update(KRYPTODL.FUNCTIONS) 
        self._BUILTINS.update(KRYPTODS.FUNCTIONS)

    def _get(self, name):
        for scope in reversed(self._scope_stack):
            if name in scope:
                return scope[name]
        if name in self._globals:
            return self._globals[name]
        raise NameError(f"KRYPTO: la variable '{name}' no está definida")

    def _set(self, name, value):
        for scope in reversed(self._scope_stack):
            if name in scope:
                scope[name] = value
                return
        self._scope_stack[-1][name] = value

    def _set_index(self, name, index, value):
        obj = self._get(name)
        if not isinstance(obj, list):
            raise TypeError(f"KRYPTO: '{name}' no es indexable")
        obj[int(index)] = value

    def _push_scope(self, bindings=None):
        self._scope_stack.append(bindings or {})

    def _pop_scope(self):
        self._scope_stack.pop()


    def visitProgram(self, ctx):
        for stmt in ctx.statement():
            self.visit(stmt)

    def visitStatement(self, ctx):
        if ctx.varDecl(): return self.visit(ctx.varDecl())
        if ctx.assignment(): return self.visit(ctx.assignment())
        if ctx.ifStatement(): return self.visit(ctx.ifStatement())
        if ctx.whileStatement(): return self.visit(ctx.whileStatement())
        if ctx.forStatement(): return self.visit(ctx.forStatement())
        if ctx.functionDecl(): return self.visit(ctx.functionDecl())
        if ctx.returnStmt(): return self.visit(ctx.returnStmt())
        if ctx.printStmt(): return self.visit(ctx.printStmt())
        if ctx.readFileStmt(): return self.visit(ctx.readFileStmt())
        if ctx.writeFileStmt(): return self.visit(ctx.writeFileStmt())
        if ctx.kryptoGraphicStmt(): return self.visit(ctx.kryptoGraphicStmt())
        if ctx.expr(): return self.visit(ctx.expr())


    def visitVarDecl(self, ctx):
        name = ctx.ID().getText()
        value = self.visit(ctx.expr()) if ctx.expr() else None
        self._set(name, value)

    def visitAssignment(self, ctx):
        name = ctx.ID().getText()
        if ctx.LBRACK(): 
            index = self.visit(ctx.expr(0))
            value = self.visit(ctx.expr(1))
            self._set_index(name, index, value)
        else:
            value = self.visit(ctx.expr(0))
            self._set(name, value)
        return value


    def visitIfStatement(self, ctx):
        condition = self.visit(ctx.expr())
        blocks = ctx.block()
        if condition:
            self.visit(blocks[0])
        elif ctx.ELSE() and len(blocks) > 1:
            self.visit(blocks[1])

    def visitWhileStatement(self, ctx):
        while self.visit(ctx.expr()):
            self.visit(ctx.block())

    def visitForStatement(self, ctx):
        self.visit(ctx.forInit())
        while self.visit(ctx.expr()):
            self.visit(ctx.block())
            self.visit(ctx.assignment())

    def visitForInit(self, ctx):
        if ctx.varDecl():
            self.visit(ctx.varDecl())
        else:
            self.visit(ctx.assignment())

    def visitBlock(self, ctx):
        for stmt in ctx.statement():
            self.visit(stmt)


    def visitFunctionDecl(self, ctx):
        name = ctx.ID().getText()
        params = []
        if ctx.paramList():
            params = [p.getText() for p in ctx.paramList().ID()]
        self._functions[name] = {"params": params, "ctx": ctx}

    def visitReturnStmt(self, ctx):
        value = self.visit(ctx.expr())
        raise _ReturnSignal(value)

    def visitFunctionCall(self, ctx):
        name = ctx.ID().getText()
        args = []
        if ctx.argList():
            args = [self.visit(e) for e in ctx.argList().expr()]

        chart = get_chart()
        _chart_dispatch = {
            'k_plot':   lambda: chart.plot(args[0], args[1]),
            'k_title':  lambda: chart.set_title(args[0]),
            'k_xlabel': lambda: chart.set_xlabel(args[0]),
            'k_ylabel': lambda: chart.set_ylabel(args[0]),
            'k_show':   lambda: chart.show(),
        }
        if name in _chart_dispatch:
            return _chart_dispatch[name]()

        if name in self._BUILTINS:
            return self._BUILTINS[name](*args)

        if name not in self._functions:
            raise NameError(f"KRYPTO: la función '{name}' no está definida")

        func = self._functions[name]
        params = func["params"]
        if len(args) != len(params):
            raise TypeError(f"KRYPTO: '{name}' espera {len(params)} argumentos, recibió {len(args)}")

        local_scope = dict(zip(params, args))
        self._push_scope(local_scope)
        result = None
        try:
            for stmt in func["ctx"].block().statement():
                self.visit(stmt)
        except _ReturnSignal as r:
            result = r.value
        finally:
            self._pop_scope()
        return result


    def visitPrintStmt(self, ctx):
        value = self.visit(ctx.expr())
        print(_krypto_repr(value))

    def visitReadFileStmt(self, ctx):
        name = ctx.ID().getText()
        path = self.visit(ctx.expr())
        value = read_file(path)
        self._set(name, value)

    def visitWriteFileStmt(self, ctx):
        path = self.visit(ctx.expr(0))
        content = self.visit(ctx.expr(1))
        write_file(path, content)

    def visitKryptoGraphicStmt(self, ctx):
        chart = get_chart()
        text = ctx.getChild(0).getText()
        if text == 'k_plot':
            x_data = self.visit(ctx.expr(0))
            y_data = self.visit(ctx.expr(1))
            chart.plot(x_data, y_data)
        elif text == 'k_title':
            chart.set_title(ctx.STRING().getText().strip('"'))
        elif text == 'k_xlabel':
            chart.set_xlabel(ctx.STRING().getText().strip('"'))
        elif text == 'k_ylabel':
            chart.set_ylabel(ctx.STRING().getText().strip('"'))
        elif text == 'k_show':
            chart.show()


    def visitOpUnaryMinus(self, ctx): return -self.visit(ctx.expr())
    def visitOpNot(self, ctx): return not self.visit(ctx.expr())
    def visitOpPow(self, ctx): return self.visit(ctx.expr(0)) ** self.visit(ctx.expr(1))

    def visitOpMulDiv(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.getChild(1).getText()
        if op == '*': return left * right
        if op == '/':
            if right == 0: raise ZeroDivisionError("KRYPTO: división por cero")
            return left / right
        if op == '%': return left % right

    def visitOpAddSub(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.getChild(1).getText()
        return left + right if op == '+' else left - right

    def visitOpCompare(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.getChild(1).getText()
        ops = {
            '==': lambda a, b: a == b,
            '!=': lambda a, b: a != b,
            '<':  lambda a, b: a < b,
            '>':  lambda a, b: a > b,
            '<=': lambda a, b: a <= b,
            '>=': lambda a, b: a >= b,
        }
        return ops[op](left, right)

    def visitOpAnd(self, ctx): return self.visit(ctx.expr(0)) and self.visit(ctx.expr(1))
    def visitOpOr(self, ctx): return self.visit(ctx.expr(0)) or self.visit(ctx.expr(1))
    def visitOpParens(self, ctx): return self.visit(ctx.expr())

    def visitOpIndex(self, ctx):
        obj = self._get(ctx.ID().getText())
        index = self.visit(ctx.expr())
        return obj[int(index)]

    def visitOpCall(self, ctx): return self.visit(ctx.functionCall())
    def visitOpList(self, ctx): return self.visit(ctx.listLiteral())
    def visitOpMatrix(self, ctx): return self.visit(ctx.matrixLiteral())
    def visitOpLiteral(self, ctx): return self.visit(ctx.literal())
    def visitOpId(self, ctx): return self._get(ctx.ID().getText())

    def visitLiteral(self, ctx):
        if ctx.NUMBER():
            text = ctx.NUMBER().getText()
            return float(text) if '.' in text else int(text)
        if ctx.STRING():
            return ctx.STRING().getText()[1:-1].encode('raw_unicode_escape').decode('unicode_escape')
        if ctx.BOOL_LIT():
            return ctx.BOOL_LIT().getText() == 'sisas'

    def visitListLiteral(self, ctx):
        return [self.visit(e) for e in ctx.expr()]

    def visitMatrixLiteral(self, ctx):
        return [self.visit(row) for row in ctx.listLiteral()]


def _krypto_repr(value):
    if isinstance(value, bool):
        return 'sisas' if value else 'nokas'
    if isinstance(value, float) and value == int(value):
        return str(int(value))
    if isinstance(value, list):
        return '[' + ', '.join(_krypto_repr(v) for v in value) + ']'
    if value is None:
        return 'nulo'
    return str(value)