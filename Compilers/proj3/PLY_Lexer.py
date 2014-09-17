from STStack import *

reserved = {
    'begin'     : 'BEGIN',
    'call'      : 'CALL',
    'const'     : 'CONST',
    'do'        : 'DO',
    'else'      : 'ELSE',
    'end'       : 'END',
    'if'        : 'IF',
    'odd'       : 'ODD',
    'print'     : 'PRINT',
    'procedure' : 'PROCEDURE',
    'read'      : 'READ',
    'then'      : 'THEN',
    'var'       : 'VAR',
    'while'     : 'WHILE',
    'write'     : 'WRITE',
    'writeln'   : 'WRITELN'
    }

tokens = ['FEND','NUM','ID','ADDOP','MULOP','RELOP','ASN','COMMENT','ENDSTMT',
          'LPAREND', 'RPAREND', 'BLCKEND', 'COMMA', 'SKIP', 'NEWLINE'] \
          + list(reserved.values())


##t_FEND      = r'\<eof>' I need to take care of EOF, I don't think I Will need it anymore
t_ASN       = r':='
t_ENDSTMT   = r';'
t_LPAREND   = r'\('
t_RPAREND   = r'\)'
t_BLCKEND   = r'\.'
t_COMMA     = r','
t_ADDOP     = r'[+-]'
t_MULOP     = r'[\*/]'
t_RELOP     = r'=|!=|<=|>=|<|>'
t_ignore    = ' \t'



def t_ID(token):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    token.type = reserved.get(token.value,'ID') #make to upper() ?
    return token

def t_NUM(token):
    r'[0-9]+'
    token.value = int(token.value)
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
    t.lexer.skip(1)
    
import ply.lex as lex

class Tokenizer:

    def __init__(self, string, SyTabManager):

        self.SyTab = SyTabManager
        self.string = string
        self.lexer = lex.lex()
        self.lexer.input(string)
        
    def t_next(self):
        tempToken = self.lexer.token()
        #build a return token out of a dict
        #IF there is no token, return none
        if tempToken == None:
            return None
        token = {'type': tempToken.type, 'value': tempToken.value, \
                 'line': tempToken.lineno}
        #token needs to search symbol table and add 'found' key
        search = self.SyTab.stackFind(token['value'])
        if (search != -1):
            return search
        #otherwise return the new token
        else:
            return token

    


if __name__ == "__main__":

    stack = symbolStack()
    stack.stackNewTable()
    dict1 = {'value':1, 'type': 'ID', 'line': 0}
    dict2 = {'value':2, 'type': 'ID', 'line': 0}
    dict3 = {'value':3, 'type': 'ID', 'line': 0}
    
    stack.stackInstall(dict1)
    stack.stackInstall(dict2)
    stack.stackInstall(dict3)
    
    testString = ''' := ; ( ) . , 1 2 3 10 100 234
begin, call, const, do, else, end, if, odd, print, procedure, read, then, var,
while, write, writeln
+ - +- * //+-*;
{this is a single line comment}
{this is a
multi line
comment}
bob
^&%$#@
'''
    lexer = Tokenizer(testString, stack)
    while True:
        token = lexer.t_next()
        if not token:
            break
        print(token)
