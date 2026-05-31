# Generated from gramatica/KryptoParser.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .KryptoParser import KryptoParser
else:
    from KryptoParser import KryptoParser

# This class defines a complete listener for a parse tree produced by KryptoParser.
class KryptoParserListener(ParseTreeListener):

    # Enter a parse tree produced by KryptoParser#program.
    def enterProgram(self, ctx:KryptoParser.ProgramContext):
        pass

    # Exit a parse tree produced by KryptoParser#program.
    def exitProgram(self, ctx:KryptoParser.ProgramContext):
        pass


    # Enter a parse tree produced by KryptoParser#statement.
    def enterStatement(self, ctx:KryptoParser.StatementContext):
        pass

    # Exit a parse tree produced by KryptoParser#statement.
    def exitStatement(self, ctx:KryptoParser.StatementContext):
        pass


    # Enter a parse tree produced by KryptoParser#varDecl.
    def enterVarDecl(self, ctx:KryptoParser.VarDeclContext):
        pass

    # Exit a parse tree produced by KryptoParser#varDecl.
    def exitVarDecl(self, ctx:KryptoParser.VarDeclContext):
        pass


    # Enter a parse tree produced by KryptoParser#type.
    def enterType(self, ctx:KryptoParser.TypeContext):
        pass

    # Exit a parse tree produced by KryptoParser#type.
    def exitType(self, ctx:KryptoParser.TypeContext):
        pass


    # Enter a parse tree produced by KryptoParser#assignment.
    def enterAssignment(self, ctx:KryptoParser.AssignmentContext):
        pass

    # Exit a parse tree produced by KryptoParser#assignment.
    def exitAssignment(self, ctx:KryptoParser.AssignmentContext):
        pass


    # Enter a parse tree produced by KryptoParser#ifStatement.
    def enterIfStatement(self, ctx:KryptoParser.IfStatementContext):
        pass

    # Exit a parse tree produced by KryptoParser#ifStatement.
    def exitIfStatement(self, ctx:KryptoParser.IfStatementContext):
        pass


    # Enter a parse tree produced by KryptoParser#whileStatement.
    def enterWhileStatement(self, ctx:KryptoParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by KryptoParser#whileStatement.
    def exitWhileStatement(self, ctx:KryptoParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by KryptoParser#forStatement.
    def enterForStatement(self, ctx:KryptoParser.ForStatementContext):
        pass

    # Exit a parse tree produced by KryptoParser#forStatement.
    def exitForStatement(self, ctx:KryptoParser.ForStatementContext):
        pass


    # Enter a parse tree produced by KryptoParser#block.
    def enterBlock(self, ctx:KryptoParser.BlockContext):
        pass

    # Exit a parse tree produced by KryptoParser#block.
    def exitBlock(self, ctx:KryptoParser.BlockContext):
        pass


    # Enter a parse tree produced by KryptoParser#functionDecl.
    def enterFunctionDecl(self, ctx:KryptoParser.FunctionDeclContext):
        pass

    # Exit a parse tree produced by KryptoParser#functionDecl.
    def exitFunctionDecl(self, ctx:KryptoParser.FunctionDeclContext):
        pass


    # Enter a parse tree produced by KryptoParser#paramList.
    def enterParamList(self, ctx:KryptoParser.ParamListContext):
        pass

    # Exit a parse tree produced by KryptoParser#paramList.
    def exitParamList(self, ctx:KryptoParser.ParamListContext):
        pass


    # Enter a parse tree produced by KryptoParser#returnStmt.
    def enterReturnStmt(self, ctx:KryptoParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by KryptoParser#returnStmt.
    def exitReturnStmt(self, ctx:KryptoParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by KryptoParser#opNot.
    def enterOpNot(self, ctx:KryptoParser.OpNotContext):
        pass

    # Exit a parse tree produced by KryptoParser#opNot.
    def exitOpNot(self, ctx:KryptoParser.OpNotContext):
        pass


    # Enter a parse tree produced by KryptoParser#opParens.
    def enterOpParens(self, ctx:KryptoParser.OpParensContext):
        pass

    # Exit a parse tree produced by KryptoParser#opParens.
    def exitOpParens(self, ctx:KryptoParser.OpParensContext):
        pass


    # Enter a parse tree produced by KryptoParser#opLiteral.
    def enterOpLiteral(self, ctx:KryptoParser.OpLiteralContext):
        pass

    # Exit a parse tree produced by KryptoParser#opLiteral.
    def exitOpLiteral(self, ctx:KryptoParser.OpLiteralContext):
        pass


    # Enter a parse tree produced by KryptoParser#opPow.
    def enterOpPow(self, ctx:KryptoParser.OpPowContext):
        pass

    # Exit a parse tree produced by KryptoParser#opPow.
    def exitOpPow(self, ctx:KryptoParser.OpPowContext):
        pass


    # Enter a parse tree produced by KryptoParser#opAddSub.
    def enterOpAddSub(self, ctx:KryptoParser.OpAddSubContext):
        pass

    # Exit a parse tree produced by KryptoParser#opAddSub.
    def exitOpAddSub(self, ctx:KryptoParser.OpAddSubContext):
        pass


    # Enter a parse tree produced by KryptoParser#opLogical.
    def enterOpLogical(self, ctx:KryptoParser.OpLogicalContext):
        pass

    # Exit a parse tree produced by KryptoParser#opLogical.
    def exitOpLogical(self, ctx:KryptoParser.OpLogicalContext):
        pass


    # Enter a parse tree produced by KryptoParser#opId.
    def enterOpId(self, ctx:KryptoParser.OpIdContext):
        pass

    # Exit a parse tree produced by KryptoParser#opId.
    def exitOpId(self, ctx:KryptoParser.OpIdContext):
        pass


    # Enter a parse tree produced by KryptoParser#opMulDiv.
    def enterOpMulDiv(self, ctx:KryptoParser.OpMulDivContext):
        pass

    # Exit a parse tree produced by KryptoParser#opMulDiv.
    def exitOpMulDiv(self, ctx:KryptoParser.OpMulDivContext):
        pass


    # Enter a parse tree produced by KryptoParser#opCall.
    def enterOpCall(self, ctx:KryptoParser.OpCallContext):
        pass

    # Exit a parse tree produced by KryptoParser#opCall.
    def exitOpCall(self, ctx:KryptoParser.OpCallContext):
        pass


    # Enter a parse tree produced by KryptoParser#opCompare.
    def enterOpCompare(self, ctx:KryptoParser.OpCompareContext):
        pass

    # Exit a parse tree produced by KryptoParser#opCompare.
    def exitOpCompare(self, ctx:KryptoParser.OpCompareContext):
        pass


    # Enter a parse tree produced by KryptoParser#functionCall.
    def enterFunctionCall(self, ctx:KryptoParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by KryptoParser#functionCall.
    def exitFunctionCall(self, ctx:KryptoParser.FunctionCallContext):
        pass


    # Enter a parse tree produced by KryptoParser#argList.
    def enterArgList(self, ctx:KryptoParser.ArgListContext):
        pass

    # Exit a parse tree produced by KryptoParser#argList.
    def exitArgList(self, ctx:KryptoParser.ArgListContext):
        pass


    # Enter a parse tree produced by KryptoParser#literal.
    def enterLiteral(self, ctx:KryptoParser.LiteralContext):
        pass

    # Exit a parse tree produced by KryptoParser#literal.
    def exitLiteral(self, ctx:KryptoParser.LiteralContext):
        pass


    # Enter a parse tree produced by KryptoParser#kryptoGraphicStmt.
    def enterKryptoGraphicStmt(self, ctx:KryptoParser.KryptoGraphicStmtContext):
        pass

    # Exit a parse tree produced by KryptoParser#kryptoGraphicStmt.
    def exitKryptoGraphicStmt(self, ctx:KryptoParser.KryptoGraphicStmtContext):
        pass



del KryptoParser