# Generated from MyGrammar.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,24,131,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,1,0,
        1,0,1,0,1,0,1,1,1,1,1,2,1,2,1,2,1,3,1,3,1,3,1,4,1,4,1,4,1,4,1,5,
        1,5,1,5,5,5,60,8,5,10,5,12,5,63,9,5,1,5,3,5,66,8,5,1,6,1,6,1,6,1,
        6,1,7,1,7,1,8,1,8,1,8,1,9,1,9,1,9,1,10,1,10,1,10,1,11,1,11,1,11,
        1,12,1,12,1,12,1,12,1,13,1,13,1,13,1,14,1,14,1,14,1,14,1,14,1,14,
        1,14,1,14,1,14,3,14,102,8,14,1,15,1,15,1,15,1,16,1,16,1,16,1,16,
        1,16,1,16,1,16,1,16,1,16,3,16,116,8,16,1,17,1,17,1,17,1,17,1,17,
        1,17,3,17,124,8,17,1,18,1,18,1,18,1,19,1,19,1,19,0,0,20,0,2,4,6,
        8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,0,1,1,0,7,10,118,
        0,40,1,0,0,0,2,44,1,0,0,0,4,46,1,0,0,0,6,49,1,0,0,0,8,52,1,0,0,0,
        10,65,1,0,0,0,12,67,1,0,0,0,14,71,1,0,0,0,16,73,1,0,0,0,18,76,1,
        0,0,0,20,79,1,0,0,0,22,82,1,0,0,0,24,85,1,0,0,0,26,89,1,0,0,0,28,
        101,1,0,0,0,30,103,1,0,0,0,32,115,1,0,0,0,34,123,1,0,0,0,36,125,
        1,0,0,0,38,128,1,0,0,0,40,41,5,1,0,0,41,42,3,2,1,0,42,43,3,4,2,0,
        43,1,1,0,0,0,44,45,5,21,0,0,45,3,1,0,0,0,46,47,5,2,0,0,47,48,3,6,
        3,0,48,5,1,0,0,0,49,50,5,3,0,0,50,51,3,8,4,0,51,7,1,0,0,0,52,53,
        5,4,0,0,53,54,3,10,5,0,54,55,3,16,8,0,55,9,1,0,0,0,56,61,3,12,6,
        0,57,58,5,5,0,0,58,60,3,12,6,0,59,57,1,0,0,0,60,63,1,0,0,0,61,59,
        1,0,0,0,61,62,1,0,0,0,62,66,1,0,0,0,63,61,1,0,0,0,64,66,1,0,0,0,
        65,56,1,0,0,0,65,64,1,0,0,0,66,11,1,0,0,0,67,68,5,21,0,0,68,69,5,
        6,0,0,69,70,3,14,7,0,70,13,1,0,0,0,71,72,7,0,0,0,72,15,1,0,0,0,73,
        74,5,11,0,0,74,75,3,18,9,0,75,17,1,0,0,0,76,77,5,12,0,0,77,78,3,
        20,10,0,78,19,1,0,0,0,79,80,3,14,7,0,80,81,3,22,11,0,81,21,1,0,0,
        0,82,83,5,13,0,0,83,84,3,24,12,0,84,23,1,0,0,0,85,86,5,14,0,0,86,
        87,3,26,13,0,87,88,3,36,18,0,88,25,1,0,0,0,89,90,3,30,15,0,90,91,
        3,28,14,0,91,27,1,0,0,0,92,93,5,15,0,0,93,94,3,30,15,0,94,95,3,28,
        14,0,95,102,1,0,0,0,96,97,5,16,0,0,97,98,3,30,15,0,98,99,3,28,14,
        0,99,102,1,0,0,0,100,102,1,0,0,0,101,92,1,0,0,0,101,96,1,0,0,0,101,
        100,1,0,0,0,102,29,1,0,0,0,103,104,3,34,17,0,104,105,3,32,16,0,105,
        31,1,0,0,0,106,107,5,17,0,0,107,108,3,34,17,0,108,109,3,32,16,0,
        109,116,1,0,0,0,110,111,5,18,0,0,111,112,3,34,17,0,112,113,3,32,
        16,0,113,116,1,0,0,0,114,116,1,0,0,0,115,106,1,0,0,0,115,110,1,0,
        0,0,115,114,1,0,0,0,116,33,1,0,0,0,117,124,5,21,0,0,118,124,5,22,
        0,0,119,120,5,4,0,0,120,121,3,26,13,0,121,122,5,11,0,0,122,124,1,
        0,0,0,123,117,1,0,0,0,123,118,1,0,0,0,123,119,1,0,0,0,124,35,1,0,
        0,0,125,126,5,19,0,0,126,127,3,38,19,0,127,37,1,0,0,0,128,129,5,
        20,0,0,129,39,1,0,0,0,5,61,65,101,115,123
    ]

class MyGrammarParser ( Parser ):

    grammarFileName = "MyGrammar.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'let'", "'='", "'{'", "'('", "','", "':'", 
                     "'Int'", "'Double'", "'Float'", "'Bool'", "')'", "'->'", 
                     "'in'", "'return'", "'+'", "'-'", "'*'", "'/'", "'}'", 
                     "';'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "ID", "NUMBER", "WS", "ANY" ]

    RULE_startRule = 0
    RULE_varName = 1
    RULE_assign = 2
    RULE_lbrace = 3
    RULE_lparen = 4
    RULE_paramList = 5
    RULE_param = 6
    RULE_typeDef = 7
    RULE_rparen = 8
    RULE_arrow = 9
    RULE_returnType = 10
    RULE_inRule = 11
    RULE_returnStmt = 12
    RULE_expr = 13
    RULE_exprTail = 14
    RULE_term = 15
    RULE_termTail = 16
    RULE_factor = 17
    RULE_closeRule = 18
    RULE_endRule = 19

    ruleNames =  [ "startRule", "varName", "assign", "lbrace", "lparen", 
                   "paramList", "param", "typeDef", "rparen", "arrow", "returnType", 
                   "inRule", "returnStmt", "expr", "exprTail", "term", "termTail", 
                   "factor", "closeRule", "endRule" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    T__18=19
    T__19=20
    ID=21
    NUMBER=22
    WS=23
    ANY=24

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class StartRuleContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def varName(self):
            return self.getTypedRuleContext(MyGrammarParser.VarNameContext,0)


        def assign(self):
            return self.getTypedRuleContext(MyGrammarParser.AssignContext,0)


        def getRuleIndex(self):
            return MyGrammarParser.RULE_startRule

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStartRule" ):
                listener.enterStartRule(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStartRule" ):
                listener.exitStartRule(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStartRule" ):
                return visitor.visitStartRule(self)
            else:
                return visitor.visitChildren(self)




    def startRule(self):

        localctx = MyGrammarParser.StartRuleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_startRule)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 40
            self.match(MyGrammarParser.T__0)
            self.state = 41
            self.varName()
            self.state = 42
            self.assign()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(MyGrammarParser.ID, 0)

        def getRuleIndex(self):
            return MyGrammarParser.RULE_varName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVarName" ):
                listener.enterVarName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVarName" ):
                listener.exitVarName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarName" ):
                return visitor.visitVarName(self)
            else:
                return visitor.visitChildren(self)




    def varName(self):

        localctx = MyGrammarParser.VarNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_varName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 44
            self.match(MyGrammarParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def lbrace(self):
            return self.getTypedRuleContext(MyGrammarParser.LbraceContext,0)


        def getRuleIndex(self):
            return MyGrammarParser.RULE_assign

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssign" ):
                listener.enterAssign(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssign" ):
                listener.exitAssign(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssign" ):
                return visitor.visitAssign(self)
            else:
                return visitor.visitChildren(self)




    def assign(self):

        localctx = MyGrammarParser.AssignContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_assign)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 46
            self.match(MyGrammarParser.T__1)
            self.state = 47
            self.lbrace()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LbraceContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def lparen(self):
            return self.getTypedRuleContext(MyGrammarParser.LparenContext,0)


        def getRuleIndex(self):
            return MyGrammarParser.RULE_lbrace

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLbrace" ):
                listener.enterLbrace(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLbrace" ):
                listener.exitLbrace(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLbrace" ):
                return visitor.visitLbrace(self)
            else:
                return visitor.visitChildren(self)




    def lbrace(self):

        localctx = MyGrammarParser.LbraceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_lbrace)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 49
            self.match(MyGrammarParser.T__2)
            self.state = 50
            self.lparen()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LparenContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def paramList(self):
            return self.getTypedRuleContext(MyGrammarParser.ParamListContext,0)


        def rparen(self):
            return self.getTypedRuleContext(MyGrammarParser.RparenContext,0)


        def getRuleIndex(self):
            return MyGrammarParser.RULE_lparen

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLparen" ):
                listener.enterLparen(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLparen" ):
                listener.exitLparen(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLparen" ):
                return visitor.visitLparen(self)
            else:
                return visitor.visitChildren(self)




    def lparen(self):

        localctx = MyGrammarParser.LparenContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_lparen)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 52
            self.match(MyGrammarParser.T__3)
            self.state = 53
            self.paramList()
            self.state = 54
            self.rparen()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def param(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MyGrammarParser.ParamContext)
            else:
                return self.getTypedRuleContext(MyGrammarParser.ParamContext,i)


        def getRuleIndex(self):
            return MyGrammarParser.RULE_paramList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParamList" ):
                listener.enterParamList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParamList" ):
                listener.exitParamList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParamList" ):
                return visitor.visitParamList(self)
            else:
                return visitor.visitChildren(self)




    def paramList(self):

        localctx = MyGrammarParser.ParamListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_paramList)
        self._la = 0 # Token type
        try:
            self.state = 65
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [21]:
                self.enterOuterAlt(localctx, 1)
                self.state = 56
                self.param()
                self.state = 61
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==5:
                    self.state = 57
                    self.match(MyGrammarParser.T__4)
                    self.state = 58
                    self.param()
                    self.state = 63
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass
            elif token in [11]:
                self.enterOuterAlt(localctx, 2)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(MyGrammarParser.ID, 0)

        def typeDef(self):
            return self.getTypedRuleContext(MyGrammarParser.TypeDefContext,0)


        def getRuleIndex(self):
            return MyGrammarParser.RULE_param

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParam" ):
                listener.enterParam(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParam" ):
                listener.exitParam(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParam" ):
                return visitor.visitParam(self)
            else:
                return visitor.visitChildren(self)




    def param(self):

        localctx = MyGrammarParser.ParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_param)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 67
            self.match(MyGrammarParser.ID)
            self.state = 68
            self.match(MyGrammarParser.T__5)
            self.state = 69
            self.typeDef()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return MyGrammarParser.RULE_typeDef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTypeDef" ):
                listener.enterTypeDef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTypeDef" ):
                listener.exitTypeDef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTypeDef" ):
                return visitor.visitTypeDef(self)
            else:
                return visitor.visitChildren(self)




    def typeDef(self):

        localctx = MyGrammarParser.TypeDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_typeDef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 71
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1920) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RparenContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def arrow(self):
            return self.getTypedRuleContext(MyGrammarParser.ArrowContext,0)


        def getRuleIndex(self):
            return MyGrammarParser.RULE_rparen

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRparen" ):
                listener.enterRparen(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRparen" ):
                listener.exitRparen(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRparen" ):
                return visitor.visitRparen(self)
            else:
                return visitor.visitChildren(self)




    def rparen(self):

        localctx = MyGrammarParser.RparenContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_rparen)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 73
            self.match(MyGrammarParser.T__10)
            self.state = 74
            self.arrow()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArrowContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def returnType(self):
            return self.getTypedRuleContext(MyGrammarParser.ReturnTypeContext,0)


        def getRuleIndex(self):
            return MyGrammarParser.RULE_arrow

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArrow" ):
                listener.enterArrow(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArrow" ):
                listener.exitArrow(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArrow" ):
                return visitor.visitArrow(self)
            else:
                return visitor.visitChildren(self)




    def arrow(self):

        localctx = MyGrammarParser.ArrowContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_arrow)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 76
            self.match(MyGrammarParser.T__11)
            self.state = 77
            self.returnType()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReturnTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def typeDef(self):
            return self.getTypedRuleContext(MyGrammarParser.TypeDefContext,0)


        def inRule(self):
            return self.getTypedRuleContext(MyGrammarParser.InRuleContext,0)


        def getRuleIndex(self):
            return MyGrammarParser.RULE_returnType

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReturnType" ):
                listener.enterReturnType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReturnType" ):
                listener.exitReturnType(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReturnType" ):
                return visitor.visitReturnType(self)
            else:
                return visitor.visitChildren(self)




    def returnType(self):

        localctx = MyGrammarParser.ReturnTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_returnType)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 79
            self.typeDef()
            self.state = 80
            self.inRule()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InRuleContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def returnStmt(self):
            return self.getTypedRuleContext(MyGrammarParser.ReturnStmtContext,0)


        def getRuleIndex(self):
            return MyGrammarParser.RULE_inRule

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInRule" ):
                listener.enterInRule(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInRule" ):
                listener.exitInRule(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInRule" ):
                return visitor.visitInRule(self)
            else:
                return visitor.visitChildren(self)




    def inRule(self):

        localctx = MyGrammarParser.InRuleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_inRule)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 82
            self.match(MyGrammarParser.T__12)
            self.state = 83
            self.returnStmt()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReturnStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(MyGrammarParser.ExprContext,0)


        def closeRule(self):
            return self.getTypedRuleContext(MyGrammarParser.CloseRuleContext,0)


        def getRuleIndex(self):
            return MyGrammarParser.RULE_returnStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReturnStmt" ):
                listener.enterReturnStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReturnStmt" ):
                listener.exitReturnStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReturnStmt" ):
                return visitor.visitReturnStmt(self)
            else:
                return visitor.visitChildren(self)




    def returnStmt(self):

        localctx = MyGrammarParser.ReturnStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_returnStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 85
            self.match(MyGrammarParser.T__13)
            self.state = 86
            self.expr()
            self.state = 87
            self.closeRule()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def term(self):
            return self.getTypedRuleContext(MyGrammarParser.TermContext,0)


        def exprTail(self):
            return self.getTypedRuleContext(MyGrammarParser.ExprTailContext,0)


        def getRuleIndex(self):
            return MyGrammarParser.RULE_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr" ):
                listener.enterExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr" ):
                listener.exitExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr" ):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)




    def expr(self):

        localctx = MyGrammarParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 89
            self.term()
            self.state = 90
            self.exprTail()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprTailContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def term(self):
            return self.getTypedRuleContext(MyGrammarParser.TermContext,0)


        def exprTail(self):
            return self.getTypedRuleContext(MyGrammarParser.ExprTailContext,0)


        def getRuleIndex(self):
            return MyGrammarParser.RULE_exprTail

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExprTail" ):
                listener.enterExprTail(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExprTail" ):
                listener.exitExprTail(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExprTail" ):
                return visitor.visitExprTail(self)
            else:
                return visitor.visitChildren(self)




    def exprTail(self):

        localctx = MyGrammarParser.ExprTailContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_exprTail)
        try:
            self.state = 101
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [15]:
                self.enterOuterAlt(localctx, 1)
                self.state = 92
                self.match(MyGrammarParser.T__14)
                self.state = 93
                self.term()
                self.state = 94
                self.exprTail()
                pass
            elif token in [16]:
                self.enterOuterAlt(localctx, 2)
                self.state = 96
                self.match(MyGrammarParser.T__15)
                self.state = 97
                self.term()
                self.state = 98
                self.exprTail()
                pass
            elif token in [11, 19]:
                self.enterOuterAlt(localctx, 3)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TermContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def factor(self):
            return self.getTypedRuleContext(MyGrammarParser.FactorContext,0)


        def termTail(self):
            return self.getTypedRuleContext(MyGrammarParser.TermTailContext,0)


        def getRuleIndex(self):
            return MyGrammarParser.RULE_term

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTerm" ):
                listener.enterTerm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTerm" ):
                listener.exitTerm(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTerm" ):
                return visitor.visitTerm(self)
            else:
                return visitor.visitChildren(self)




    def term(self):

        localctx = MyGrammarParser.TermContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_term)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 103
            self.factor()
            self.state = 104
            self.termTail()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TermTailContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def factor(self):
            return self.getTypedRuleContext(MyGrammarParser.FactorContext,0)


        def termTail(self):
            return self.getTypedRuleContext(MyGrammarParser.TermTailContext,0)


        def getRuleIndex(self):
            return MyGrammarParser.RULE_termTail

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTermTail" ):
                listener.enterTermTail(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTermTail" ):
                listener.exitTermTail(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTermTail" ):
                return visitor.visitTermTail(self)
            else:
                return visitor.visitChildren(self)




    def termTail(self):

        localctx = MyGrammarParser.TermTailContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_termTail)
        try:
            self.state = 115
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [17]:
                self.enterOuterAlt(localctx, 1)
                self.state = 106
                self.match(MyGrammarParser.T__16)
                self.state = 107
                self.factor()
                self.state = 108
                self.termTail()
                pass
            elif token in [18]:
                self.enterOuterAlt(localctx, 2)
                self.state = 110
                self.match(MyGrammarParser.T__17)
                self.state = 111
                self.factor()
                self.state = 112
                self.termTail()
                pass
            elif token in [11, 15, 16, 19]:
                self.enterOuterAlt(localctx, 3)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FactorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(MyGrammarParser.ID, 0)

        def NUMBER(self):
            return self.getToken(MyGrammarParser.NUMBER, 0)

        def expr(self):
            return self.getTypedRuleContext(MyGrammarParser.ExprContext,0)


        def getRuleIndex(self):
            return MyGrammarParser.RULE_factor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFactor" ):
                listener.enterFactor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFactor" ):
                listener.exitFactor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFactor" ):
                return visitor.visitFactor(self)
            else:
                return visitor.visitChildren(self)




    def factor(self):

        localctx = MyGrammarParser.FactorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_factor)
        try:
            self.state = 123
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [21]:
                self.enterOuterAlt(localctx, 1)
                self.state = 117
                self.match(MyGrammarParser.ID)
                pass
            elif token in [22]:
                self.enterOuterAlt(localctx, 2)
                self.state = 118
                self.match(MyGrammarParser.NUMBER)
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 3)
                self.state = 119
                self.match(MyGrammarParser.T__3)
                self.state = 120
                self.expr()
                self.state = 121
                self.match(MyGrammarParser.T__10)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CloseRuleContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def endRule(self):
            return self.getTypedRuleContext(MyGrammarParser.EndRuleContext,0)


        def getRuleIndex(self):
            return MyGrammarParser.RULE_closeRule

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCloseRule" ):
                listener.enterCloseRule(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCloseRule" ):
                listener.exitCloseRule(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCloseRule" ):
                return visitor.visitCloseRule(self)
            else:
                return visitor.visitChildren(self)




    def closeRule(self):

        localctx = MyGrammarParser.CloseRuleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_closeRule)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 125
            self.match(MyGrammarParser.T__18)
            self.state = 126
            self.endRule()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EndRuleContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return MyGrammarParser.RULE_endRule

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEndRule" ):
                listener.enterEndRule(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEndRule" ):
                listener.exitEndRule(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEndRule" ):
                return visitor.visitEndRule(self)
            else:
                return visitor.visitChildren(self)




    def endRule(self):

        localctx = MyGrammarParser.EndRuleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_endRule)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 128
            self.match(MyGrammarParser.T__19)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





