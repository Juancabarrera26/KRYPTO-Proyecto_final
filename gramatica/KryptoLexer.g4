lexer grammar KryptoLexer;

// --- PALABRAS RESERVADAS ---
IF       : 'krif';
ELSE     : 'krelse';
WHILE    : 'krloop';
FOR      : 'krfor';
FUNCTION : 'krfunc';
RETURN   : 'yield';
STOP     : 'stop';
PRINT    : 'kprint';
READ_F   : 'kread';
WRITE_F  : 'kwrite';

// --- TIPOS DE DATOS ---
INT_T     : 'num';
FLOAT_T   : 'dec';
BOOL_T    : 'logic';
STRING_T  : 'text';
LIST_T    : 'chain';
MATRIX_T  : 'grid';
DICC_T    : 'vault';

// --- LITERALES ---
BOOL_LIT : 'sisas' | 'nokas';
NUMBER   : [0-9]+ ('.' [0-9]+)?;
STRING   : '"' (~["\r\n])* '"';

// --- IDENTIFICADORES ---
ID : [a-zA-Z_][a-zA-Z0-9_]*;

// --- OPERADORES ARITMÉTICOS ---
PLUS   : '+';
MINUS  : '-';
MUL    : '*';
DIV    : '/';
MOD    : '%';
POW    : '^';
ASSIGN : '=';

// --- PUNTUACIÓN ---
COMMA  : ',';
SEMI   : ';';
DOT    : '.';

// --- AGRUPADORES ---
LPAREN : '(';
RPAREN : ')';
LBRACK : '[';
RBRACK : ']';
LBRACE : '{';
RBRACE : '}';

// --- OPERADORES LÓGICOS Y COMPARACIÓN ---
EQ  : '==';
NEQ : '!=';
LE  : '<=';
GE  : '>=';
LT  : '<';
GT  : '>';
OR  : '||';
AND : '&&';
NOT : '!';

// --- TOKENS GRÁFICOS ---
PLOTVAG   : 'k_plot';
SHOWVAG   : 'k_show';
TITLEVAG  : 'k_title';
XLABELVAG : 'k_xlabel';
YLABELVAG : 'k_ylabel';

// --- COMENTARIOS Y ESPACIOS ---
COMMENT       : '//' ~[\r\n]* -> skip;
BLOCK_COMMENT : '/*' .*? '*/' -> skip;
WS            : [ \t\r\n]+ -> skip;
