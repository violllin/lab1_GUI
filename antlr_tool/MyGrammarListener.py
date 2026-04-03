# Generated from MyGrammar.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .MyGrammarParser import MyGrammarParser
else:
    from MyGrammarParser import MyGrammarParser

# This class defines a complete listener for a parse tree produced by MyGrammarParser.
class MyGrammarListener(ParseTreeListener):

    # Enter a parse tree produced by MyGrammarParser#startRule.
    def enterStartRule(self, ctx:MyGrammarParser.StartRuleContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#startRule.
    def exitStartRule(self, ctx:MyGrammarParser.StartRuleContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#varName.
    def enterVarName(self, ctx:MyGrammarParser.VarNameContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#varName.
    def exitVarName(self, ctx:MyGrammarParser.VarNameContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#assign.
    def enterAssign(self, ctx:MyGrammarParser.AssignContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#assign.
    def exitAssign(self, ctx:MyGrammarParser.AssignContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#lbrace.
    def enterLbrace(self, ctx:MyGrammarParser.LbraceContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#lbrace.
    def exitLbrace(self, ctx:MyGrammarParser.LbraceContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#lparen.
    def enterLparen(self, ctx:MyGrammarParser.LparenContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#lparen.
    def exitLparen(self, ctx:MyGrammarParser.LparenContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#paramList.
    def enterParamList(self, ctx:MyGrammarParser.ParamListContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#paramList.
    def exitParamList(self, ctx:MyGrammarParser.ParamListContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#param.
    def enterParam(self, ctx:MyGrammarParser.ParamContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#param.
    def exitParam(self, ctx:MyGrammarParser.ParamContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#typeDef.
    def enterTypeDef(self, ctx:MyGrammarParser.TypeDefContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#typeDef.
    def exitTypeDef(self, ctx:MyGrammarParser.TypeDefContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#rparen.
    def enterRparen(self, ctx:MyGrammarParser.RparenContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#rparen.
    def exitRparen(self, ctx:MyGrammarParser.RparenContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#arrow.
    def enterArrow(self, ctx:MyGrammarParser.ArrowContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#arrow.
    def exitArrow(self, ctx:MyGrammarParser.ArrowContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#returnType.
    def enterReturnType(self, ctx:MyGrammarParser.ReturnTypeContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#returnType.
    def exitReturnType(self, ctx:MyGrammarParser.ReturnTypeContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#inRule.
    def enterInRule(self, ctx:MyGrammarParser.InRuleContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#inRule.
    def exitInRule(self, ctx:MyGrammarParser.InRuleContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#returnStmt.
    def enterReturnStmt(self, ctx:MyGrammarParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#returnStmt.
    def exitReturnStmt(self, ctx:MyGrammarParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#expr.
    def enterExpr(self, ctx:MyGrammarParser.ExprContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#expr.
    def exitExpr(self, ctx:MyGrammarParser.ExprContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#exprTail.
    def enterExprTail(self, ctx:MyGrammarParser.ExprTailContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#exprTail.
    def exitExprTail(self, ctx:MyGrammarParser.ExprTailContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#term.
    def enterTerm(self, ctx:MyGrammarParser.TermContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#term.
    def exitTerm(self, ctx:MyGrammarParser.TermContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#termTail.
    def enterTermTail(self, ctx:MyGrammarParser.TermTailContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#termTail.
    def exitTermTail(self, ctx:MyGrammarParser.TermTailContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#factor.
    def enterFactor(self, ctx:MyGrammarParser.FactorContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#factor.
    def exitFactor(self, ctx:MyGrammarParser.FactorContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#closeRule.
    def enterCloseRule(self, ctx:MyGrammarParser.CloseRuleContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#closeRule.
    def exitCloseRule(self, ctx:MyGrammarParser.CloseRuleContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#endRule.
    def enterEndRule(self, ctx:MyGrammarParser.EndRuleContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#endRule.
    def exitEndRule(self, ctx:MyGrammarParser.EndRuleContext):
        pass



del MyGrammarParser