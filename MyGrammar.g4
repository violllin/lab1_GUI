grammar MyGrammar;

startRule    : 'let' varName assign ;
varName      : ID ;
assign       : '=' lbrace ;
lbrace       : '{' lparen ;
lparen       : '(' paramList rparen ;
paramList    : param (',' param)* | /* пусто */ ;
param        : ID ':' typeDef ;
typeDef      : 'Int' | 'Double' | 'Float' | 'Bool' ;
rparen       : ')' arrow ;
arrow        : '->' returnType ;
returnType   : typeDef inRule ;
inRule       : 'in' returnStmt ;
returnStmt   : 'return' expr closeRule ;
expr         : term exprTail ;
exprTail     : '+' term exprTail
             | '-' term exprTail
             | /* пусто */ ;
term         : factor termTail ;
termTail     : '*' factor termTail
             | '/' factor termTail
             | /* пусто */ ;
factor       : ID
             | NUMBER
             | '(' expr ')' ;
closeRule    : '}' endRule ;
endRule      : ';' ;

ID           : [a-zA-Z] [a-zA-Z0-9]* ;
NUMBER       : [0-9]+ ;
WS           : [ \t\r\n]+ -> skip ;