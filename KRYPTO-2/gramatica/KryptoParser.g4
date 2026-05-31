parser grammar KryptoParser;
options { tokenVocab=KryptoLexer; }

// -------- RAÍZ --------
program
    : statement* EOF
    ;

// -------- SENTENCIAS --------
statement
    : varDecl SEMI
    | assignment SEMI
    | ifStatement
    | whileStatement
    | forStatement
    | functionDecl
    | returnStmt SEMI
    | printStmt SEMI
    | readFileStmt SEMI
    | writeFileStmt SEMI
    | kryptoGraphicStmt
    | expr SEMI
    ;

// -------- TIPOS --------
type
    : INT_T
    | FLOAT_T
    | BOOL_T
    | STRING_T
    | LIST_T
    | MATRIX_T
    | DICC_T
    ;

// -------- DECLARACIÓN Y ASIGNACIÓN --------
varDecl
    : type ID (ASSIGN expr)?
    ;

assignment
    : ID ASSIGN expr                    // simple: x = expr
    | ID LBRACK expr RBRACK ASSIGN expr // indexed: x[i] = expr
    ;

// -------- CONTROL DE FLUJO --------
ifStatement
    : IF LPAREN expr RPAREN block (ELSE block)? STOP
    ;

whileStatement
    : WHILE LPAREN expr RPAREN block STOP
    ;

forStatement
    : FOR LPAREN forInit SEMI expr SEMI assignment RPAREN block STOP
    ;

forInit
    : varDecl
    | assignment
    ;

// -------- BLOQUES --------
block
    : LBRACE statement* RBRACE
    ;

// -------- FUNCIONES --------
functionDecl
    : FUNCTION ID LPAREN paramList? RPAREN block STOP
    ;

paramList
    : ID (COMMA ID)*
    ;

returnStmt
    : RETURN expr
    ;

// -------- I/O --------
printStmt
    : PRINT LPAREN expr RPAREN
    ;

readFileStmt
    : type ID ASSIGN READ_F LPAREN expr RPAREN
    ;

writeFileStmt
    : WRITE_F LPAREN expr COMMA expr RPAREN
    ;

// -------- EXPRESIONES (precedencia correcta, mayor a menor) --------
expr
    : MINUS expr                                            # opUnaryMinus
    | NOT expr                                              # opNot
    | expr POW expr                                         # opPow
    | expr (MUL | DIV | MOD) expr                          # opMulDiv
    | expr (PLUS | MINUS) expr                             # opAddSub
    | expr (EQ | NEQ | LT | GT | LE | GE) expr            # opCompare
    | expr AND expr                                         # opAnd
    | expr OR expr                                          # opOr
    | LPAREN expr RPAREN                                    # opParens
    | ID LBRACK expr RBRACK                                # opIndex
    | functionCall                                          # opCall
    | listLiteral                                           # opList
    | matrixLiteral                                         # opMatrix
    | literal                                               # opLiteral
    | ID                                                    # opId
    ;

// -------- LLAMADAS --------
functionCall
    : ID LPAREN argList? RPAREN
    ;

argList
    : expr (COMMA expr)*
    ;

// -------- LITERALES --------
literal
    : NUMBER
    | STRING
    | BOOL_LIT
    ;

listLiteral
    : LBRACK (expr (COMMA expr)*)? RBRACK
    ;

matrixLiteral
    : LBRACK listLiteral (COMMA listLiteral)* RBRACK
    ;

// -------- GRÁFICAS ASCII --------
kryptoGraphicStmt
    : PLOTVAG LPAREN expr COMMA expr RPAREN SEMI
    | TITLEVAG LPAREN STRING RPAREN SEMI
    | XLABELVAG LPAREN STRING RPAREN SEMI
    | YLABELVAG LPAREN STRING RPAREN SEMI
    | SHOWVAG LPAREN RPAREN SEMI
    ;
