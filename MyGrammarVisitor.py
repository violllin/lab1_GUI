# Generated from MyGrammar.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .MyGrammarParser import MyGrammarParser
else:
    from MyGrammarParser import MyGrammarParser

# This class defines a complete generic visitor for a parse tree produced by MyGrammarParser.

class MyGrammarVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MyGrammarParser#startRule.
    def visitStartRule(self, ctx:MyGrammarParser.StartRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#varName.
    def visitVarName(self, ctx:MyGrammarParser.VarNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#assign.
    def visitAssign(self, ctx:MyGrammarParser.AssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#lbrace.
    def visitLbrace(self, ctx:MyGrammarParser.LbraceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#lparen.
    def visitLparen(self, ctx:MyGrammarParser.LparenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#paramList.
    def visitParamList(self, ctx:MyGrammarParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#param.
    def visitParam(self, ctx:MyGrammarParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#typeDef.
    def visitTypeDef(self, ctx:MyGrammarParser.TypeDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#rparen.
    def visitRparen(self, ctx:MyGrammarParser.RparenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#arrow.
    def visitArrow(self, ctx:MyGrammarParser.ArrowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#returnType.
    def visitReturnType(self, ctx:MyGrammarParser.ReturnTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#inRule.
    def visitInRule(self, ctx:MyGrammarParser.InRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#returnStmt.
    def visitReturnStmt(self, ctx:MyGrammarParser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#expr.
    def visitExpr(self, ctx:MyGrammarParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#exprTail.
    def visitExprTail(self, ctx:MyGrammarParser.ExprTailContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#term.
    def visitTerm(self, ctx:MyGrammarParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#termTail.
    def visitTermTail(self, ctx:MyGrammarParser.TermTailContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#factor.
    def visitFactor(self, ctx:MyGrammarParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#closeRule.
    def visitCloseRule(self, ctx:MyGrammarParser.CloseRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#endRule.
    def visitEndRule(self, ctx:MyGrammarParser.EndRuleContext):
        return self.visitChildren(ctx)



del MyGrammarParser