import ply.lex as lex
from STStack import *
'''
makes use of the PLY module
'''
'''
Check list:
    make much more comprehensive examples of miniPascal
    enclose the lexer in a class
        -next() method
        -get and use a symbol table
            -modify ID to search the symbol table
    write a stand-in parser
    write a main
'''
class Lexer:

    def __init__(self, string, table):
        
        self.symbolTable = table
        self.lexer = lex.lex()
        self.lexer.input(string)  

    def nextToken(self):
        
        token = self.lexer.token()
        if token == None:
            return None
            
        search = self.symbolTable.stackFind(token.value)
        if (search != -1):
            return search
        else:
            return token

reserved = {
    'program'   : 'PROG',
    'var'       : 'VAR',
    'array'     : 'ARR',
    'integer'   : 'INT',
    'real'      : 'REAL',
    'function'  : 'FUNC',
    'procedure' : 'PROC',
    'begin'     : 'BEG',
    'end'       : 'END',
    'READ'      : 'READ',
    'WRITE'     : 'WRITE',
    'WRITELN'   : 'WRITELN',
    'if'        : 'IF',
    'then'      : 'THEN',
    'else'      : 'ELSE',
    'while'     : 'WHILE',
    'do'        : 'DO',
    'of'        : 'OF',
    'not'       : 'NOT'
    }
    
tokens = [ 'EOF',
           'ID',
           'NUM',
           'ASSIGNOP',
           'RELOP',
           'ADDOP',
           'MULOP',
           'DOTDOT'
           ] + list(reserved.values())
             
t_DOTDOT        = r'\.\.'
t_ASSIGNOP      = r':='
t_RELOP         = r'<>|<=|>=|<|>|='
t_ADDOP         = r'[+-]'
t_MULOP         = r'[\*/]'
t_NUM           =r'(\d+)(\.\d+)?(E[+-]?(\d+))?'
t_ignore        = ' \t'


literals = [ ':',
             ';',
             '[',
             ']',
             '(',
             ')',
             ',',
             '.'
             ]
          
def t_EOF(token):
    r'\<eof>'
    return token
    
def t_ID(token):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    token.value = token.value.lower()
    
    #doesn't want this here
    if token.value in ['or']: # If the ID is an 'or' make the token an ADDOP
        token.type = reserved.get(token.value,'ADDOP')
        return token   
        
    if token.value in ['div', 'mod', 'and']: # If the ID is 'div', 'mod', or 'and' 
                                             # make the token a MULOP
        token.type = reserved.get(token.value,'MULOP')
        return token

    token.type = reserved.get(token.value,'ID')
    return token
    
def t_COMMENT(token):
    r'\{[^\}]*\}'
    newlines = token.value.count('\n')
    token.lexer.lineno += newlines   

def t_NEWLINE(token):
    r'\n'
    token.lexer.lineno += len(token.value)

def t_error(t):
    print ("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)#do not do, return characters to parser
    

    
#=========================================================================
if __name__ == "__main__":
    teststring =    '''
program example;
var x, y: integer;
function gcd(a, b: integer): integer;
begin
    if b = 0 then gcd := a
    else gcd := gcd(b, a mod b)
end; 

begin
    read(x, y);
    write(gcd(x,y))
end.
'''
 
    syTab = symbolStack()
    syTab.stackNewTable()
    
    lexer = Lexer(teststring, syTab)
    
    token = lexer.nextToken()
    while token != None:
        if type( token ) == tuple:
            syTab.stackInstall(token[1])
        else:
            syTab.stackInstall(token)
        token = lexer.nextToken()
        
    print(syTab)    
    teststring = '''
iF thEn id program ; , vAr : ARRAY [ ] of integer real funCtion procedure ( )
begin end := else while do read write writeln + - * / = <> < <= > >= or DIV Mod
and 1 2 3 4 5 6 7 8 9 10 100 1000 1.1 1.2 10.1 10.10 1E1 1.1E1 10.10E10 1.3E+3
10.10E-100 .. .
amod anid anthen arrayThen 1goodthing10others +-*/ 
{ this is a multiline test
there are comments all over teh place
blah

}
{ single line comment}
token
'''
    print()
    syTab = symbolStack()
    syTab.stackNewTable()
    
    lexer = Lexer(teststring, syTab)
    
    token = lexer.nextToken()
    while token != None:
        if type( token ) == tuple:
            syTab.stackInstall(token[1])
        else:
            syTab.stackInstall(token)
        token = lexer.nextToken()
        
    print(syTab) 
        