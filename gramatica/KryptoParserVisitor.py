# Generated from KryptoParser.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .KryptoParser import KryptoParser
else:
    from KryptoParser import KryptoParser

# This class defines a complete generic visitor for a parse tree produced by KryptoParser.

class KryptoParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by KryptoParser#program.
    def visitProgram(self, ctx:KryptoParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#statement.
    def visitStatement(self, ctx:KryptoParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#type.
    def visitType(self, ctx:KryptoParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#varDecl.
    def visitVarDecl(self, ctx:KryptoParser.VarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#assignment.
    def visitAssignment(self, ctx:KryptoParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#ifStatement.
    def visitIfStatement(self, ctx:KryptoParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#whileStatement.
    def visitWhileStatement(self, ctx:KryptoParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#forStatement.
    def visitForStatement(self, ctx:KryptoParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#forInit.
    def visitForInit(self, ctx:KryptoParser.ForInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#block.
    def visitBlock(self, ctx:KryptoParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#functionDecl.
    def visitFunctionDecl(self, ctx:KryptoParser.FunctionDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#paramList.
    def visitParamList(self, ctx:KryptoParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#returnStmt.
    def visitReturnStmt(self, ctx:KryptoParser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#printStmt.
    def visitPrintStmt(self, ctx:KryptoParser.PrintStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#readFileStmt.
    def visitReadFileStmt(self, ctx:KryptoParser.ReadFileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#writeFileStmt.
    def visitWriteFileStmt(self, ctx:KryptoParser.WriteFileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#opUnaryMinus.
    def visitOpUnaryMinus(self, ctx:KryptoParser.OpUnaryMinusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#opNot.
    def visitOpNot(self, ctx:KryptoParser.OpNotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#opParens.
    def visitOpParens(self, ctx:KryptoParser.OpParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#opLiteral.
    def visitOpLiteral(self, ctx:KryptoParser.OpLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#opAnd.
    def visitOpAnd(self, ctx:KryptoParser.OpAndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#opList.
    def visitOpList(self, ctx:KryptoParser.OpListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#opPow.
    def visitOpPow(self, ctx:KryptoParser.OpPowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#opId.
    def visitOpId(self, ctx:KryptoParser.OpIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#opMulDiv.
    def visitOpMulDiv(self, ctx:KryptoParser.OpMulDivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#opCall.
    def visitOpCall(self, ctx:KryptoParser.OpCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#opCompare.
    def visitOpCompare(self, ctx:KryptoParser.OpCompareContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#opMatrix.
    def visitOpMatrix(self, ctx:KryptoParser.OpMatrixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#opOr.
    def visitOpOr(self, ctx:KryptoParser.OpOrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#opAddSub.
    def visitOpAddSub(self, ctx:KryptoParser.OpAddSubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#opIndex.
    def visitOpIndex(self, ctx:KryptoParser.OpIndexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#functionCall.
    def visitFunctionCall(self, ctx:KryptoParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#argList.
    def visitArgList(self, ctx:KryptoParser.ArgListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#literal.
    def visitLiteral(self, ctx:KryptoParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#listLiteral.
    def visitListLiteral(self, ctx:KryptoParser.ListLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#matrixLiteral.
    def visitMatrixLiteral(self, ctx:KryptoParser.MatrixLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KryptoParser#kryptoGraphicStmt.
    def visitKryptoGraphicStmt(self, ctx:KryptoParser.KryptoGraphicStmtContext):
        return self.visitChildren(ctx)



del KryptoParser